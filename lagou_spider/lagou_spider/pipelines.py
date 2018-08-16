# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from lagou_spider.items import engine, Base
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)

class StoragePipeline(object):

    def open_spider(self, spider):
        session = Session()
        Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        return item