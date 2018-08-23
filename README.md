# LagouSpider

### 基本情况
* 在原计划中，该爬虫是想使用`Scrapy`中的`CrawlSpider`模板创建`spider`，因为从网页来看，[拉勾网](https://www.lagou.com/)作为一个互联网求职网站结构具有一定规律性，从关键词搜索得到职位清单页，之后每一个职位的介绍页和相应公司页面应该都是相似的，所以使用`CrawlSpider`中的`Rule`属性可以为爬取这样结构具有统一性的网站提供便利；然而在实际通过浏览器对网页进行分析后发现，拉勾网做了比较好的反爬措施，，通过工具直接访问（除非使用Selenium）是无法获取有效页面的，而对于数十页的职位信息也不能一味地使用`Selenium`；对目标网站页面进行进一步分析后发现，职位消息和基本的用于布局的页面文件是分开来传输的，职位信息以`Json`文件的形式在浏览器开发者工具`Network->XHR`标签中显示( *https://www.lagou.com/jobs/positionAjax.json?city=杭州&needAddtionalResult=false* )，通过简单查阅资料得知这是`AJAX`请求的知识，目的是对网页进行异步更新

    > XMLHttpRequest 是 AJAX 的基础。
    
    > XMLHttpRequest 用于在后台与服务器交换数据。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。
    
* 了解到这些后，爬虫便有了方向，但是`CrawlSpider`模板就不能用了，便重新创建了一个爬虫文件`lagou.py`

* 经过试验可以知道 *https://www.lagou.com/jobs/positionAjax.json?city=杭州&needAddtionalResult=false* 直接访问网址会报错

    > `{"success": false, "msg": "您操作太频繁,请稍后再访问", "clientIp": "39.188.225.98"}`
    
* 通过浏览器可知，如果要成功访问该`URL`，需要以`POST`方法请求，并且需要带上头部信息（谨慎起见也可带`Cookie`信息），并且提交表单数据为`first`来表示是否为首页、`pn`来表示当前为第几页、`kd`来表示目前职位的关键词是什么，了解了这些以后就能够按照一定逻辑编写爬虫代码（为了获取`Cookie`信息，仍然在`start_requests`中使用`Selenium`进行模拟访问获得`Cookies`值）

* 值得注意的是该爬虫的`item`需要的数据涉及职位清单页以及相应的职位详情页，所以在`parse_list`方法解析玩清单页后，将`item`信息携带在`meta`中传给了`parse_jobs`方法，然后通过两个解析函数为`item`补充值

* 最后，该爬虫数据存储使用了`MySQL`数据库，由于`SQL`语句容易由于不熟悉而出错，这里使用了第三方库`SQLAlchemy`，将构建`model`的嵌套于`item`类中，从而实现可以通过在不同爬虫组件之间传递的`item`来调用数据库模型类

* 以上基本完成爬虫的构建

### 完成改进

* 在爬取过程中发现爬虫很容易被目标网站判定为爬虫并被迫中止正常爬取工作，最开始是通过在每次在解析函数抛出`item`或者`request`时设置`time.sleep`函数来放缓爬取过程，后通过阅读文档发现在`settings`文件中可以设置自动限速，启用默认的设置，基本就能够达到爬虫正常运行
    > 礼貌爬虫
* 其他的改进，主要是`UserAgent`和`proxy`的设置，但是仍然使用的[西刺代理（国内高匿代理）](http://www.xicidaili.com/nn)所以出现大量`ip`不可用，故暂且不设置代理
