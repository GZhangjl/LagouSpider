# -*- coding: utf-8 -*-


"""
由于本来认为拉勾网整布局具有一定规律，适合使用CrawlSpider模板做爬取，但是在遇到反爬手段后，认为已经失去原先认为的规律，故该文件作废，
改用普通Spider模板进行爬取。
"""

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.http import Request, FormRequest
from selenium import webdriver
import time

from lagou_spider.items import LagouSpiderItem


class LagouSpider(CrawlSpider):
    name = 'lagou_fail'
    allowed_domains = ['lagou.com']
    #登陆页面，用于模拟登陆，但是实际情况应该不许登陆也能够浏览职位列表页和详情页
    login_url = 'https://passport.lagou.com/login/login.html'
    #以下页面为列表页json文件，正常使用爬虫访问拉勾网搜索页面返回结果中无法显示职位信息（被隐藏），通过查看浏览器开发者工具发现该json文件
    #但是该链接如果浏览器正常打开会显示访问过于频繁提醒页，故需要结合headers信息等模拟访问
    #另外，可发现，该json文件访问方法为POST，而非GET
    start_urls = ['https://www.lagou.com/jobs/positionAjax.json?px=default&city=杭州&positionName=python&needAddtionalResult=false']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        # 'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&city=%E6%9D%AD%E5%B7%9E',
        # 'Referer': 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?oquery=%E7%88%AC%E8%99%AB&fromSearch=true&labelWords=relative&city=%E6%9D%AD%E5%B7%9E',
        # 'Cookie': 'JSESSIONID=ABAAABAAAFCAAEGBA8A016409CD5A94308B5758353D5250; user_trace_token=20180813132134-ede9b748-5cd8-4eba-9978-7ea55f4c497b; _ga=GA1.2.2018058031.1534137697; _gid=GA1.2.2137491042.1534137697; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1534137697; LGUID=20180813132135-bf357d5b-9eb8-11e8-a37b-5254005c3644; X_HTTP_TOKEN=56d4d91c6b655446a10c108166aeaed7; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; index_location_city=%E5%85%A8%E5%9B%BD; LG_LOGIN_USER_ID=93b926a609c6d5a8bde947aee251e08c6fc889ed40f10955; _putrc=C808C49F2427ED22; login=true; unick=%E5%BC%A0%E4%BF%8A%E4%BA%AE; gate_login_token=f8bb44a1f747281891f86187146273b4fba0eb00b715c996; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1534144986; LGRID=20180813152304-b7a18d01-9ec9-11e8-bb51-525400f775ce; TG-TRACK-CODE=index_search; SEARCH_ID=875b40d1648f407f98b3565da58337f3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }



    rules = (
        Rule(LinkExtractor(allow='https://www.lagou.com/jobs/\d+.html$'), callback='parse_jobs', follow=True),
        Rule(LinkExtractor(restrict_css='div.pager_container>a:last-child'), callback='parse_pages', follow=True),
    )

    def start_requests(self):
        #
        # web_driver = webdriver.Chrome(r'C:\Users\zhang\chromedriver_win32\chromedriver.exe')
        # web_driver.get(url=self.login_url)
        # web_driver.find_element_by_css_selector('div[data-view=passwordLogin]>form>div:first-child>input').send_keys('zhangjl_0912@163.com')
        # web_driver.find_element_by_css_selector('input[type=password]').send_keys('HJW13XD53zjl')
        # web_driver.find_element_by_css_selector('div[data-view=passwordLogin]>form>div:last-child>input').click()
        # time.sleep(10)
        # web_driver.find_element_by_css_selector('form#searchForm input[type=text]').send_keys('python')
        # web_driver.find_element_by_css_selector('form#searchForm input[type=submit]').click()
        # time.sleep(15)
        # ori_cookies = web_driver.get_cookies()
        # cookies = {}
        # for cookie in ori_cookies:
        #     cookies[cookie['name']] = cookie['value']
        # web_driver.close()

        yield FormRequest(url=self.start_urls[0], method='POST', formdata={'first':'true','pn':'1','kd':'python'}, callback=self.parse, headers=self.headers)

    def parse_jobs(self, response):
        item_loader = ItemLoader(LagouSpiderItem,response=response)
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

    def parse_pages(self, response):
        pass