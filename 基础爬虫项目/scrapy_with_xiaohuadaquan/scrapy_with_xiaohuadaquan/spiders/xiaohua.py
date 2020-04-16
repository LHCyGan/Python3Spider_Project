# -*- coding: utf-8 -*-
import scrapy


class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['xiaohua.zol.com.cn/']
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
               "Referer": "http://xiaohua.zol.com.cn/"}

    def start_requests(self):

        start_urls = ['http://xiaohua.zol.com.cn//']
        for url in start_urls:
            yield scrapy.Request(url, headers=XiaohuaSpider.headers, callback=self.parse)

    def parse(self, response):
        filename = 'xiaohua.txt'
        with open(filename, 'w', encoding='utf8') as f:
            # tag = response.xpath('//ul[@class="scrapy_with_news163-list"]/li[1]/a[1]').extract()[0]
            # content = response.xpath("//ul[@class='scrapy_with_news163-list']/li[1]/a[2]/text()").extract()[0]
            xiaohua = response.xpath('/html/body/div[5]/div[1]/div[2]/ul/li')
            for con in xiaohua:
                tag = response.xpath('/html/body/div[5]/div[1]/div[2]/ul/li/a[1]').extract()
                content = response.xpath('/html/body/div[5]/div[1]/div[2]/ul/li/a[2]').extract()
                print(content, tag)
                f.write(str(content) + '\n')