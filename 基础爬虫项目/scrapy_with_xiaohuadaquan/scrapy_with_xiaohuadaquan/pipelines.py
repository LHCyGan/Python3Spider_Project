# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

class ScrapyWithXiaohuadaquanPipeline(object):
    def __init__(self):
        self.file = open('news_data.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self):
        # 关闭进程和文件
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        # 开启spider
        self.exporter.export_item(item)
        return item
