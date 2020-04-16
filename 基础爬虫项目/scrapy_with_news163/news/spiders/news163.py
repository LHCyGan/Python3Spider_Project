# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_with_news163.news import items


# url格式
# https://news.163.com/20/0330/12/F8VETKE4000189FH.html

class News163Spider(CrawlSpider):
    name = 'news163'
    allowed_domains = ['www.news163.com']
    start_url = ['http://www.news163.com']
    rules = (
        Rule(LinkExtractor(allow=r'https://news.163.com/20/0330/\d+/.*?.html'),
             callback='parse_item', follow=True)
    )

    def parse_item(self, response):
        item = items.NewsItem()
        item['news_thread'] = response.url.strip().split('/')[-1][:-5]
        self.get_title(response, item)
        self.get_time(response, item)
        self.get_source(response, item)
        self.get_source_url(response, item)
        self.get_news(response, item)
        return item

    def get_title(self, response, item):
        title = response.css('title::text').extract()[0]
        if title:
            print(title)
            item['news_title'] = title

    def get_time(self, response, item):
        time = response.xpath('//div[@class="post_time_source"]/text()').extract()[0]
        if time:
            print("time: " + time.strip().replace('来源：', '').replace('\n3000', ''))
            item['news_time'] = time

    def get_source(self, response, item):
        source = response.css('a#ne_article_source::text').extract()[0]
        if source:
            print('source: ' + source)
            item['news_source'] = source

    def get_source_url(self, response, item):
        source_url = response.css('a#ne_article_source::attr(href)').extract()[0]
        if source_url:
            print("来源地址： " + source_url)
            item['source_url'] = source_url

    def get_news(self, response, item):
        news = response.css('.post_text p::text').extract()[0]
        if news:
            item['news_body'] = news