import re
import time
import json
from datetime import datetime

from selenium import webdriver
from scrapy import Selector
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from jd_spider.models import *

chrome_options = Options()

#设置headless模式
# chrome_options.add_argument("--headless")
# 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--disable-gpu')
#设置不加载图片
chrome_options.add_argument("blink-settings=imagesEnabled=false")

browser = webdriver.Chrome(executable_path="E:/爬虫0基础入门/chromedriver_win32/chromedriver.exe", chrome_options=chrome_options)

#1. 无界面启动selenium
#2. 设置selenium不加载图片

def process_value(nums_str):
    """
    将字符串类型的数字转换成数字
    :param nums_str: 字符串类型的数字，数字中可能包含"万"
    :return: 成功返回数字，默认返回0
    """
    nums = 0
    re_math = re.search("(\d+)", nums_str)
    if re_math:
        nums = int(re_math.group(1))
        if "万" in nums_str:
            nums *= 10000
    return nums


def parse_good(good_id):
    browser.get("https://item.jd.com/{}.html".format(good_id))

    sel = Selector(text=browser.page_source)

    #提取商品的基本信息
    good = Good(id=good_id)
    name = "".join(sel.xpath("//div[@class='sku-name']/text()").extract()).strip()
    price = float("".join(sel.xpath("//span[@class='price J-p-{}']/text()".format(good_id)).extract()).strip())

    detail = "".join(sel.xpath("//div[@id='detail']//div[@class='tab-con']").extract())
    good_images = sel.xpath("//div[@id='spec-list']//img/@src").extract()
    supplier_info = "".join(sel.xpath("//div[@id='summary-service']").extract())

    re_match = re.search('<a href="//(.*).jd.com', supplier_info)
    if re_match:
        good.supplier = re_match.group(1)
    else:
        good.supplier = "京东"

    good.name = name
    good.price = price
    good.content = detail
    good.image_list = json.dumps(good_images)

    #模拟点击规格和包装
    ggbz_ele = browser.find_element_by_xpath("//div[@class='tab-main large']//li[contains(text(), '规格与包装')]")
    ggbz_ele.click()
    time.sleep(3)
    sel = Selector(text=browser.page_source)
    ggbz_detail = "".join(sel.xpath("//div[@id='detail']/div[@class='tab-con']").extract())
    good.ggbz = ggbz_detail

    #模拟点击商品评价后获取评价的信息
    sppj_ele = browser.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|shangpinpingjia_1']")
    sppj_ele.click()
    time.sleep(5)
    sel = Selector(text=browser.page_source)
    tag_list = sel.xpath("//div[@class='tag-list tag-available']//span/text()").extract()
    good_rate = int(sel.xpath("//div[@class='percent-con']/text()").extract()[0])
    good.good_rate = good_rate

    summary_as = sel.xpath("//ul[@class='filter-list']/li/a")
    for summary in summary_as:
        name = summary.xpath("./text()").extract()[0]
        nums = summary.xpath("./em/text()").extract()[0]
        nums = process_value(nums)

        if name == "晒图":
            good.has_image_comment_nums = nums
        elif name == "视频晒单":
            good.has_video_comment_nums = nums
        elif name == "追评":
            good.has_add_comment_nums = nums
        elif name == "好评":
            good.well_comment_nums = nums
        elif name == "中评":
            good.middle_comment_nums = nums
        elif name == "差评":
            good.bad_comment_nums = nums
        elif name == "全部评价":
            good.comments_nums = nums

    #保存商品信息
    existed_good = Good.select().where(Good.id == good.id)
    if existed_good:
        good.save()
    else:
        good.save(force_insert=True)

    for tag in tag_list:
        re_match = re.match("(.*)\((\d+)\)", tag)
        if re_match:
            tag_name = re_match.group(1)
            nums = int(re_match.group(2))

            existed_summarys = GoodEvaluateSummary.select().where(GoodEvaluateSummary.good==good, GoodEvaluateSummary.tag==tag_name)
            if existed_summarys:
                summary = existed_summarys[0]
            else:
                summary = GoodEvaluateSummary(good=good)

            summary.tag = tag_name
            summary.num = nums
            summary.save()

    #获取商品的评价
    has_next_page = True
    while has_next_page:
        all_evalutes = sel.xpath("//div[@class='comment-item']")
        for item in all_evalutes:
            good_evaluate = GoodEvaluate(good=good)

            evaluate_id = item.xpath("./@data-guid").extract()[0]
            print(evaluate_id)
            good_evaluate.id = evaluate_id
            user_head_url = item.xpath(".//div[@class='user-info']//img/@src").extract()[0]
            user_name = "".join(item.xpath(".//div[@class='user-info']/text()").extract()).strip()

            good_evaluate.user_head_url = user_head_url
            good_evaluate.user_name = user_name

            star = item.xpath("./div[2]/div[1]/@class").extract()[0]
            star = int(star[-1])
            good_evaluate.star = star
            evaluate = "".join(item.xpath("./div[2]/p[1]/text()").extract()[0]).strip()
            good_evaluate.content = evaluate

            image_list = item.xpath("./div[2]//div[@class='pic-list J-pic-list']/a/img/@src").extract()
            video_list = item.xpath("./div[2]//div[@class='J-video-view-wrap clearfix']//video/@src").extract()

            good_evaluate.image_list = json.dumps(image_list)
            good_evaluate.video_list = json.dumps(video_list)

            praised_nums = int(item.xpath(".//div[@class='comment-op']/a[2]/text()").extract()[0])
            comment_nums = int(item.xpath(".//div[@class='comment-op']/a[3]/text()").extract()[0])

            good_evaluate.praised_nums = praised_nums
            good_evaluate.comment_nums = comment_nums

            comment_info = item.xpath(".//div[@class='order-info']/span/text()").extract()
            order_info = comment_info[:-1]
            evaluate_time = comment_info[-1]
            good_evaluate.good_info = json.dumps(order_info)
            evaluate_time = datetime.strptime(evaluate_time, "%Y-%m-%d %H:%M")
            good_evaluate.evaluate_time = evaluate_time

            #保存评价信息
            existed_good_evaluates = GoodEvaluate.select().where(GoodEvaluate.id==good_evaluate.id)
            if existed_good_evaluates:
                good_evaluate.save()
            else:
                good_evaluate.save(force_insert=True)

        try:
            next_page_ele = browser.find_element_by_xpath("//div[@id='comment']//a[@class='ui-pager-next']")
            # next_page_ele.click()
            next_page_ele.send_keys("\n")
            time.sleep(5)
            sel = Selector(text=browser.page_source)
        except NoSuchElementException as e:
            has_next_page = False












if __name__ == "__main__":
    parse_good(7652013)
