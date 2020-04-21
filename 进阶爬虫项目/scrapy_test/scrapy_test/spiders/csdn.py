from urllib import parse
from datetime import datetime
import re

import scrapy

from scrapy_test.models import *
from scrapy_test.items import *


class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ['csdn.net']
    start_urls = ['https://bbs.csdn.net/forums/ios']
    domain = "https://bbs.csdn.net"

    def parse(self, response):
        all_trs = response.xpath("//table[@class='forums_tab_table']//tr")[2:]
        for tr in all_trs:
            # topic = Topic()
            topic_item = TopicItem()

            if tr.xpath(".//td[1]/span/text()").extract():
                status = tr.xpath(".//td[1]/span/text()").extract()[0]
                topic_item["status"] = status
            if tr.xpath(".//td[2]/em/text()").extract():
                score = tr.xpath(".//td[2]/em/text()").extract()[0]
                topic_item["score"] = int(score)
            topic_url = parse.urljoin(self.domain, tr.xpath(".//td[3]/a/@href").extract()[0])
            topic_title = tr.xpath(".//td[3]/a/text()").extract()[0]
            author_url = parse.urljoin(self.domain, tr.xpath(".//td[4]/a/@href").extract()[0])
            author_id = author_url.split("/")[-1]
            create_time = tr.xpath(".//td[4]/em/text()").extract()[0]
            create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M")
            answer_info = tr.xpath(".//td[5]/span/text()").extract()[0]
            answer_nums = answer_info.split("/")[0]
            click_nums = answer_info.split("/")[1]
            last_time_str = tr.xpath(".//td[6]/em/text()").extract()[0]
            last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M")

            topic_item["id"] = int(topic_url.split("/")[-1])
            topic_item["title"] = topic_title
            topic_item["author"] = author_id
            topic_item["click_nums"] = int(click_nums)
            topic_item["answer_nums"] = int(answer_nums)
            topic_item["create_time"] = create_time
            topic_item["last_answer_time"] = last_time
            topic_item["content"] = ""
            
            # yield topic_item
            # existed_topics = Topic.select().where(Topic.id == topic.id)
            # if existed_topics:
            #     topic.save()
            # else:
            #     topic.save(force_insert=True)

            yield scrapy.http.Request(url=topic_url, callback=self.parse_topic)
            yield scrapy.http.Request(url=author_url, callback=self.parse_author)

        next_page = response.xpath("//a[@class='pageliststy next_page']/@href").extract()
        if next_page:
            next_url = parse.urljoin(self.domain, next_page[0])
            yield scrapy.http.Request(url=next_url, callback=self.parse)

    def parse_topic(self, response):
        # 获取帖子的详情以及回复
        url = response.url
        topic_id = url.split("/")[-1]
        all_divs = response.xpath("//div[starts-with(@id, 'post-')]")
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

        next_page = response.xpath("//a[@class='pageliststy next_page']/@href").extract()
        if next_page:
            next_url = parse.urljoin(self.domain, next_page[0])
            yield scrapy.http.Request(url=next_url, callback=self.parse_topic)

    def parse_author(self, response):
        url = response.url
        author_id = url.split("/")[-1]
        # 获取用户的详情
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        }
        author = Author()
        author.id = author_id
        all_li_strs = response.xpath("//ul[@class='mod_my_t clearfix']/li/span/text()").extract()
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

        desc = response.xpath("//dd[@class='user_desc']/text()").extract()
        if desc:
            author.desc = desc[0].strip()
        person_b = response.xpath("//dd[@class='person_b']/ul/li")
        for item in person_b:
            item_text = "".join(item.extract())
            if "csdnc-m-add" in item_text:
                location = item.xpath(".//span/text()").extract()[0].strip()
                author.location = location
            else:
                industry = item.xpath(".//span/text()").extract()[0].strip()
                author.industry = industry
        name = response.xpath("//h4[@class='username']/text()").extract()[0]
        author.name = name.strip()
        existed_author = Author.select().where(Author.id == author_id)
        if existed_author:
            author.save()
        else:
            author.save(force_insert=True)