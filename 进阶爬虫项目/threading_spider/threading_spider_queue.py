from threading import Thread
from urllib import parse
from datetime import datetime
import ast
import re
import time
from queue import Queue

import requests
from scrapy import Selector

from csdn_spider.models import *

topic_list_queue = Queue(maxsize=10)
topic_queue = Queue(maxsize=10)
author_queue = Queue(maxsize=10)
domain = "https://bbs.csdn.net"


def get_nodes_json():
    left_menu_text = requests.get("https://bbs.csdn.net/dynamic_js/left_menu.js?csdn").text
    nodes_str_match = re.search("forumNodes: (.*])", left_menu_text)
    if nodes_str_match:
        nodes_str = nodes_str_match.group(1).replace("null", "None")
        nodes_list = ast.literal_eval(nodes_str)
        return nodes_list
    return []

url_list = []
def process_nodes_list(nodes_list):
    #将js的格式提取出url到list中
    for item in nodes_list:
        if "url" in item:
            if item["url"]:
                url_list.append(item["url"])
            if "children" in item:
                process_nodes_list(item["children"])

def get_level1_list(nodes_list):
    level1_url = []
    for item in nodes_list:
        if "url" in item and item["url"]:
            level1_url.append(item["url"])

    return level1_url

def get_last_urls():
    #获取最终需要抓取的url
    nodes_list = get_nodes_json()
    process_nodes_list(nodes_list)
    level1_url = get_level1_list(nodes_list)
    last_urls = []
    for url in url_list:
        if url not in level1_url:
            last_urls.append(url)
    all_urls = []
    for url in last_urls:
        all_urls.append(parse.urljoin(domain, url))
        all_urls.append(parse.urljoin(domain, url+"/recommend"))
        all_urls.append(parse.urljoin(domain, url+"/closed"))
    return all_urls


class ParseTopicDetailThread(Thread):
    def run(self):
        while 1:
            url = topic_queue.get()
            print("开始获取帖子：{}".format(url))

            # 获取帖子的详情以及回复
            topic_id = url.split("/")[-1]
            res_text = requests.get(url).text
            sel = Selector(text=res_text)
            all_divs = sel.xpath("//div[starts-with(@id, 'post-')]")
            topic_item = all_divs[0]
            content = topic_item.xpath(".//div[@class='post_body post_body_min_h']").extract()[0]
            praised_nums = topic_item.xpath(".//label[@class='red_praise digg']//em/text()").extract()[0]
            jtl_str = topic_item.xpath(".//div[@class='close_topic']/text()").extract()[0]
            jtl = 0
            jtl_match = re.search("(\d+)%", jtl_str)
            if jtl_match:
                jtl = int(jtl_match.group(1))
            existed_topics = Topic.select().where(Topic.id == topic_id)
            if existed_topics:
                topic = existed_topics[0]
                topic.content = content
                topic.jtl = jtl
                topic.praised_nums = praised_nums
                topic.save()

            for answer_item in all_divs[1:]:
                answer = Answer()
                answer.topic_id = topic_id
                author_info = answer_item.xpath(".//div[@class='nick_name']//a[1]/@href").extract()[0]
                author_id = author_info.split("/")[-1]
                create_time = answer_item.xpath(".//label[@class='date_time']/text()").extract()[0]
                create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")
                answer.author = author_id
                answer.create_time = create_time
                praised_nums = topic_item.xpath(".//label[@class='red_praise digg']//em/text()").extract()[0]
                answer.parised_nums = int(praised_nums)
                content = topic_item.xpath(".//div[@class='post_body post_body_min_h']").extract()[0]
                answer.content = content

                answer.save()

            next_page = sel.xpath("//a[@class='pageliststy next_page']/@href").extract()
            if next_page:
                topic_queue.put(next_page[0])


class ParseAuthorThread(Thread):
    def run(self):
        while 1:
            url = author_queue.get()
            print("开始获取用户：{}".format(url))
            author_id = url.split("/")[-1]
            # 获取用户的详情
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            }
            res_text = requests.get(url, headers=headers).text
            sel = Selector(text=res_text)
            author = Author()
            author.id = author_id
            all_li_strs = sel.xpath("//ul[@class='mod_my_t clearfix']/li/span/text()").extract()
            click_nums = all_li_strs[0]
            original_nums = all_li_strs[1]
            forward_nums = int(all_li_strs[2])
            rate = int(all_li_strs[3])
            answer_nums = int(all_li_strs[4])
            parised_nums = int(all_li_strs[5])

            author.click_nums = click_nums
            author.original_nums = original_nums
            author.forward_nums = forward_nums
            author.rate = rate
            author.answer_nums = answer_nums
            author.parised_nums = parised_nums

            desc = sel.xpath("//dd[@class='user_desc']/text()").extract()
            if desc:
                author.desc = desc[0].strip()
            person_b = sel.xpath("//dd[@class='person_b']/ul/li")
            for item in person_b:
                item_text = "".join(item.extract())
                if "csdnc-m-add" in item_text:
                    location = item.xpath(".//span/text()").extract()[0].strip()
                    author.location = location
                else:
                    industry = item.xpath(".//span/text()").extract()[0].strip()
                    author.industry = industry
            name = sel.xpath("//h4[@class='username']/text()").extract()[0]
            author.name = name.strip()
            existed_author = Author.select().where(Author.id == author_id)
            if existed_author:
                author.save()
            else:
                author.save(force_insert=True)


class ParseTopicListThread(Thread):
    def run(self):
        while 1:
            #1. 先判断一下ctrl命令
            #2. 如果接收到了ctrl+c命令，如何优雅的退出， topic_list_queue队列里面的数据是否应该保存起来(mysql， 文件当中)
            url = topic_list_queue.get(timeout=3)
            print("开始获取帖子列表页：{}".format(url))

            res_text = requests.get(url).text
            sel = Selector(text=res_text)
            all_trs = sel.xpath("//table[@class='forums_tab_table']/tbody//tr")[2:]
            index = 0
            for tr in all_trs:
                index += 1
                topic = Topic()

                if tr.xpath(".//td[1]/span/text()").extract():
                    status = tr.xpath(".//td[1]/span/text()").extract()[0]
                    topic.status = status
                if tr.xpath(".//td[2]/em/text()").extract():
                    score = tr.xpath(".//td[2]/em/text()").extract()[0]
                    topic.score = int(score)
                topic_title = tr.xpath(".//td[3]/a/text()").extract()[0]
                if len(tr.xpath(".//td[3]/a/@href").extract()) == 2:
                    topic_url = parse.urljoin(domain, tr.xpath(".//td[3]/a/@href").extract()[1])
                else:
                    topic_url = parse.urljoin(domain, tr.xpath(".//td[3]/a/@href").extract()[0])
                author_url = parse.urljoin(domain, tr.xpath(".//td[4]/a/@href").extract()[0])
                author_id = author_url.split("/")[-1]
                create_time = tr.xpath(".//td[4]/em/text()").extract()[0]
                create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M")
                answer_info = tr.xpath(".//td[5]/span/text()").extract()[0]
                answer_nums = answer_info.split("/")[0]
                click_nums = answer_info.split("/")[1]
                last_time_str = tr.xpath(".//td[6]/em/text()").extract()[0]
                last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M")

                topic.id = int(topic_url.split("/")[-1])
                topic.title = topic_title
                topic.author = author_id
                topic.click_nums = int(click_nums)
                topic.answer_nums = int(answer_nums)
                topic.create_time = create_time
                topic.last_answer_time = last_time
                existed_topics = Topic.select().where(Topic.id == topic.id)
                if existed_topics:
                    topic.save()
                else:
                    topic.save(force_insert=True)

                topic_queue.put(topic_url)
                author_queue.put(author_url)

            next_page = sel.xpath("//a[@class='pageliststy next_page']/@href").extract()
            if next_page:
                next_url = parse.urljoin(domain, next_page[0])
                topic_list_queue.put(next_url)


if __name__ == "__main__":
    #1. 将获取初始(导航栏)的url放到一个单独的线程去完成
    #2. 如何去停止线程
    #1. 我们想手动停止 ctrl+c 很优雅的退出
        #1 .接收ctrl+c
        #2. 保存临时变量
        #3. 下一次启动程序的时候，我们是应该如何从文件(mysql)中启动
    #2. 程序有可能直接崩溃
        #1. queue是内存中的，是否安全
        #2. queue这种模式就不合适了， 使用msyql来同步
        #3. redis
    #3. 爬虫完成以后的退出
        #如何去判断爬虫数据已经抓取完成了
    #积极思考如何改进业务

    last_urls = get_last_urls()
    for url in last_urls:
        topic_list_queue.put(url)

    topic_list_thread = ParseTopicListThread()
    topic_detail_thread = ParseTopicDetailThread()
    author_thread = ParseAuthorThread()

    topic_detail_thread.start()
    topic_list_thread.start()
    author_thread.start()
