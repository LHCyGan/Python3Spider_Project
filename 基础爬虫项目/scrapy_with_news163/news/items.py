# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义爬取字段
    news_thread = scrapy.Field()
    news_title = scrapy.Field()
    news_time = scrapy.Field()
    news_source = scrapy.Field()
    source_url = scrapy.Field()
    news_body = scrapy.Field()
