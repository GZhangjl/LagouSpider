# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker

from lagou_spider.items import sql_engine, Base


Session = sessionmaker(sql_engine)

class StoragePipeline(object):

    def open_spider(self, spider):
        self.session = Session()
        Base.metadata.create_all(sql_engine)

    def modify_html(self, text):
        from w3lib.html import remove_tags
        res = ' '.join(remove_tags(text).split('\n')).strip()
        return res

    def process_item(self, item, spider):
        item['job_adv'] = '/'.join(item['job_adv'])
        item['job_comp_label'] = '/'.join(item['job_comp_label'])
        item['job_descr'] = self.modify_html(item['job_descr'])
        item['job_position'] = '/'.join(item['job_position'])

        one_job = item.LagouJob(id=item['job_id'], url=item['job_url'], company=item['job_company'], name=item['job_name'],
                      salary=item['job_salary'], city=item['job_city'], worky=item['job_worky'], edu=item['job_edu'],
                      nature=item['job_nature'], adv=item['job_adv'], descr=item['job_descr'], district=item['job_district'],
                      position=item['job_position'], comp_label=item['job_comp_label'], comp_url=item['job_comp_url'])
        self.session.add(one_job)
        # self.session.merge(one_job)
        self.session.commit()

    def close_spider(self, spider):
        self.session.close_all()