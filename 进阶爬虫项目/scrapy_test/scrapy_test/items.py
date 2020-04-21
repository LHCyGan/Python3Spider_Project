# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_test.models import *

class ScrapyTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TopicItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    id = scrapy.Field()
    author = scrapy.Field()
    create_time = scrapy.Field()
    answer_nums = scrapy.Field()
    click_nums = scrapy.Field()
    praised_nums = scrapy.Field()
    jtl = scrapy.Field()  # 结帖率
    score = scrapy.Field()  # 赏分
    status = scrapy.Field() # 状态
    last_answer_time = scrapy.Field()

    def save(self):
        topic = Topic()
        topic.title = self["title"]
        topic.content = self["content"]
        topic.id = self["id"]
        topic.author = self["author"]
        topic.create_time = self["create_time"]
        topic.answer_nums = self.get("answer_nums", 0)
        topic.click_nums = self.get("click_nums", 0)
        topic.praised_nums = self.get("praised_nums", 0)
        topic.jtl = self.get("jtl", 0)
        topic.score = self.get("score", 0)
        topic.status = self["status"]
        topic.last_answer_time = self["last_answer_time"]

        existed_topics = Topic.select().where(Topic.id == topic.id)
        if existed_topics:
            topic.save()
        else:
            topic.save(force_insert=True)