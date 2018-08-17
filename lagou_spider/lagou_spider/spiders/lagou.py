# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request, HtmlResponse
import time

from lagou_spider.items import LagouSpiderItem

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    ent_url = 'https://www.lagou.com/jobs/list_Python?px=default&city=%E6%9D%AD%E5%B7%9E'# 杭州
    temp_job_url = 'https://www.lagou.com/jobs/{0}.html'
    temp_comp_url = 'https://www.lagou.com/gongsi/{0}.html'
    start_urls = ['https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            # 'lagou_spider.middlewares.ProxyDownloaderMiddleware': 2,
            'lagou_spider.middlewares.UserAgentDownloaderMiddleware': 1
        },
        'SET_UA': 'random'
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&city=%E6%9D%AD%E5%B7%9E',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    COOKIES_DICT = {}

    def start_requests(self):
        from selenium.webdriver import Chrome
        import random

        web_driver = Chrome(executable_path=r'C:\Users\zhang\chromedriver_win32\chromedriver.exe')
        web_driver.get(url=self.ent_url)
        time.sleep(5)
        page_source = web_driver.page_source
        page_response = HtmlResponse(url=self.ent_url, body=page_source, encoding='utf8')
        cookies = web_driver.get_cookies()
        web_driver.close()

        for cookie in cookies:
            LagouSpider.COOKIES_DICT[cookie['name']] = cookie['value']

        all_page = page_response.css('div.pager_container>span:nth-last-child(2)::text').extract_first().strip()
        all_page = int(all_page)
        for i in range(1,all_page+1):
            # time.sleep(8)
            is_first = 'true' if i == 1 else 'false'
            formdata = {'first': is_first, 'pn': str(i),'kd':'python'}

            time.sleep(random.randrange(1,6))
            yield FormRequest(url=self.start_urls[0], formdata=formdata, callback=self.parse_list,
                              cookies=LagouSpider.COOKIES_DICT, headers=self.headers)

    def parse_jobs(self, response):
        job_item = response.meta['item']
        descr = response.css('.description+div').extract_first()
        job_item['job_descr'] = descr
        yield job_item

    def parse_list(self, response):
        import json


        jobs = json.loads(response.text)
        jobs_content = jobs['content']
        jobs_results = jobs_content['positionResult']['result']
        for job in jobs_results:
            # 注意：Item的实例化一定要在for循环里面，否则的话，当前一个item被抛出去的同时，由于后一个item正在修改实例（由于整个系统
            # 是异步的），同时这是一个cpu密集型的操作，速度非常快，所以会有极大概率出现不同的item里面的内容相互混乱，当id一样时就会因
            # 为“主键冲突”无法写入数据库。
            job_item = LagouSpiderItem()
            job_item['job_id'] = job['positionId']
            job_url = self.temp_job_url.format(job['positionId'])
            job_item['job_url'] = job_url
            job_item['job_company'] = job['companyFullName']
            job_item['job_name'] = job['positionName']
            job_item['job_salary'] = job['salary']
            job_item['job_city'] = job['city']
            job_item['job_worky'] = job['workYear']
            job_item['job_edu'] = job['education']
            job_item['job_nature'] = job['jobNature']
            job_item['job_adv'] = job['companyLabelList']
            job_item['job_district'] = job['district']
            job_item['job_position'] = job['positionLables']
            job_item['job_comp_label'] = job['companyLabelList']
            job_comp_url = self.temp_comp_url.format(job['companyId'])
            job_item['job_comp_url'] = job_comp_url

            # yield self.job_item

            # time.sleep(5)
            yield Request(url=job_url, callback=self.parse_jobs, method='GET', meta={'item':job_item}, headers=self.headers,
                          cookies=LagouSpider.COOKIES_DICT)