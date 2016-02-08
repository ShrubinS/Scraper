import scrapy
from datetime import datetime
import logging
from twisted.python import log
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from amazon.items import AmazonItem

class DmozSpider(CrawlSpider):
    name = "amazon"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["http://www.amazon.com/s?ie=UTF8&page=1&rh=n%3A2407749011%2Ck%3Amobile%20phones"
    ]
    
    def __init__(self, name=None, **kwargs):       
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        rootLogger = logging.getLogger()
        fileHandler = logging.FileHandler("{0}.log".format(self.name))
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)
        super(DmozSpider, self).__init__(name, **kwargs)
    
    def parse(self, response):
        for next_url in response.xpath('//*[@id="pagnNextLink"]/@href'):
            url_complete = response.urljoin(next_url.extract())
        for href in response.xpath('//*[@class="s-result-item  celwidget "]/div/div[2]/div[1]/a/@href'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_items)
        yield scrapy.Request(url_complete, callback=self.parse)    

    def parse_items(self, response):
        items = AmazonItem()
        items['title'] = response.xpath('.//*[@id="productTitle"]/text()').extract()
        items['features'] = response.xpath('.//*[@id="feature-bullets"]/ul//li/span/text()').extract()
        items['product_url'] = response.url
        items['image_urls'] = response.xpath('.//*[@id="landingImage"]/@src').extract()
        yield items
       
        