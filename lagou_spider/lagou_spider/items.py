# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, CHAR, INT, TEXT

sql_engine = create_engine('mysql://root:root@localhost:3306/lagou?charset=utf8',echo=True)
Base = declarative_base()

class LagouSpiderItem(scrapy.Item):

    job_id = scrapy.Field()
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

    class LagouJob(Base):

        __tablename__ = 'lagouJob'

        id = Column(INT(), primary_key=True)
        url = Column(CHAR(40), nullable=False)  # e.g. https://www.lagou.com/jobs/4900858.html
        company = Column(VARCHAR(20), nullable=False)
        name = Column(VARCHAR(50), nullable=False)
        salary = Column(VARCHAR(10), nullable=False)
        city = Column(CHAR(3), nullable=False)
        worky = Column(VARCHAR(10), nullable=False)
        edu = Column(CHAR(5), nullable=False)
        nature = Column(CHAR(5), nullable=False)
        adv = Column(TEXT(50))
        descr = Column(TEXT(200))
        district = Column(CHAR(10))
        position = Column(TEXT(50))
        comp_label = Column(TEXT(50))
        comp_url = Column(CHAR(40))
