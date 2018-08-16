# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request, HtmlResponse
import time

from lagou_spider.items import LagouSpiderItem, ItemLoader

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
            time.sleep(5)
            is_first = 'true' if i == 1 else 'false'
            formdata = {'first': is_first, 'pn': str(i),'kd':'python'}
            yield FormRequest(url=self.start_urls[0], formdata=formdata, callback=self.parse_list, meta={'index':i}, headers=self.headers)

    def parse_jobs(self, response):
        descr = response.css('.description+div').extract_first()
        self.job_item['job_descr'] = descr
        yield self.job_item

    def parse_list(self, response):
        import json
        self.job_item = LagouSpiderItem()

        jobs = json.loads(response.text)
        jobs_content = jobs['content']
        jobs_results = jobs_content['positionResult']['result']
        for job in jobs_results:
            job_url = self.temp_job_url.format(job['positionId'])
            self.job_item['job_url'] = job_url
            self.job_item['job_company'] = job['companyFullName']
            self.job_item['job_name'] = job['positionName']
            self.job_item['job_salary'] = job['salary']
            self.job_item['job_city'] = job['city']
            self.job_item['job_worky'] = job['workYear']
            self.job_item['job_edu'] = job['education']
            self.job_item['job_nature'] = job['jobNature']
            self.job_item['job_adv'] = job['companyLabelList']
            self.job_item['job_district'] = job['district']
            self.job_item['job_position'] = job['positionLables']
            self.job_item['job_comp_label'] = job['companyLabelList']
            job_comp_url = self.temp_comp_url.format(job['companyId'])
            self.job_item['job_comp_url'] = job_comp_url

            time.sleep(5)
            yield Request(url=job_url, callback=self.parse_jobs, method='GET', headers=self.headers,
                          cookies=LagouSpider.COOKIES_DICT)