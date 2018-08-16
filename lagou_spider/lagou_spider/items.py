# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:root@localhost:3306/zhihu?charset=utf8',echo=True)
Base = declarative_base()

class LagouJob(Base):

    __tablename__ = 'lagouJob'

    pass

class LagouSpiderItem(scrapy.Item):

    job_url = scrapy.Field()
    job_company = scrapy.Field()
    job_name = scrapy.Field()
    job_salary = scrapy.Field()
    job_city = scrapy.Field()
    job_worky = scrapy.Field()
    job_edu = scrapy.Field()
    job_nature = scrapy.Field()
    job_adv = scrapy.Field()
    job_descr = scrapy.Field()
    job_district = scrapy.Field()
    job_position = scrapy.Field()
    job_comp_label = scrapy.Field()
    job_comp_url = scrapy.Field()

    # define the fields for your item here like:
    # name = scrapy.Field()
    def item_member(self):
        return LagouJob()
