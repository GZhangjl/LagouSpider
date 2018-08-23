# LagouSpider

### 基本情况

* 该爬虫最初是想使用`Scrapy`中的`CrawlSpider`模板来创建`spider`，因为从整体来看，[拉勾网](https://www.lagou.com/)作为一个互联网求职网站，其结构具有一定规律性，从关键词搜索得到职位清单页，然后每一个职位的介绍页和相应公司的页面的布局都是相似的，所以使用`CrawlSpider`中的`Rule`属性可以为爬取这样的网站提供便利；然而在实际通过浏览器对网页进行分析后发现，拉勾网做了较好的反爬措施，通过爬虫代码直接访问（除非使用Selenium）是无法获取有效页面的，而对于数十页的职位信息也不能一味地使用`Selenium`

* 对目标网站进一步分析后发现，职位信息和布局页面文件是分开来传输的，职位信息以`Json`文件的形式在浏览器开发者工具`Network->XHR`标签中显示( *https://www.lagou.com/jobs/positionAjax.json?city=杭州&needAddtionalResult=false* )，通过简单查阅资料得知这是`AJAX`请求的知识，目的是对网页进行异步更新

    > XMLHttpRequest 是 AJAX 的基础。XMLHttpRequest 用于在后台与服务器交换数据。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。
    
* 了解到这些后，爬虫便有了方向，但是`CrawlSpider`模板就不能用了，便重新创建了一个爬虫`lagou`

* 经过试验可以知道直接访问 *https://www.lagou.com/jobs/positionAjax.json?city=杭州&needAddtionalResult=false* 会提示请求错误

    > `{"success": false, "msg": "您操作太频繁,请稍后再访问", "clientIp": "****（本机ip）"}`
    
* 通过浏览器可知，如果要成功访问该`URL`，需要以`POST`方法请求，并且需要带上头部信息（谨慎起见也可带`Cookie`信息），并且携带表单数据，表单数据中`first`来表示是否为首页（值为`true`或`false`）、`pn`来表示当前为第几页（值为数字）、`kd`来表示目前职位的关键词是什么（本爬虫为`python`）；了解了这些以后就能够按照一定逻辑编写爬虫代码（在`start_requests`中使用`Selenium`进行模拟访问获得`Cookie`信息）

* 值得注意的是，该爬虫`item`需要的数据涉及职位清单页以及相应的职位详情页，所以在`parse_list`方法解析完清单页后，将`item`信息携带在`meta`中传递给`parse_jobs`方法，两个解析函数共同为完成`item`

* 最后，该爬虫数据存储使用了`MySQL`数据库，由于`SQL`语句容易出错，所以这里使用了第三方库`SQLAlchemy`，将构建的`model`嵌套于`item`类中，从而实现通过在不同爬虫组件之间传递`item`来调用数据库模型类

* 以上基本完成爬虫的构建

### 完成改进

* 在爬取过程中发现爬虫很容易被目标网站判定为爬虫并被迫中止爬取工作，为了解决这个问题，最开始是通过在每次解析函数抛出`item`或者`request`前设置`time.sleep`函数来放缓请求过程，后来通过阅读文档发现在`settings`文件中可以设置自动限速`AUTOTHROTTLE`相关属性，启用默认的设置，基本就能够达到爬虫正常运行

    > 礼貌爬虫

* 其他的改进，主要是`UserAgent`和`proxy`设置，但是代理`ip`仍然使用的[西刺代理（国内高匿代理）](http://www.xicidaili.com/nn)，所以出现大量`ip`不可用，故暂且不设置代理
