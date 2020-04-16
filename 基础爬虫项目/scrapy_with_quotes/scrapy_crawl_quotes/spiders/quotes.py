# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    # 自动构造域名
    allowed_domains = ['quotes.toscrape.com']
    # # 构造 url
    # start_urls = ['http://quotes.toscrape.com/page/1/',
    #               'http://quotes.toscrape.com/page/2/']

    def start_requests(self):
        # 构造 url
        start_urls = ['http://quotes.toscrape.com/page/1/',
                      'http://quotes.toscrape.com/page/2/']
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'quotes-{}.txt'.format(page)
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        #     # 输出日志
        #     self.log('Saved file {}'.format(filename))
        with open(filename, 'w', encoding='utf8') as f:
            quotes = response.css('.quote')
            for quote in quotes:
                title = quote.css('.text::text').extract()[0]
                author = quote.css('.author::text').extract()[0]
                tag = quote.css('.tag::text').extract()[0]
                print('title:\n' + (title))
                print('author:\n' + author)
                print('tag:\n' + tag)
                f.write(author + '\t' + title + '\t' + tag + '\n')
