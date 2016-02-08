import scrapy
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
    
    rules = (
        Rule(LxmlLinkExtractor(allow=(), restrict_xpaths=('//a[@id="pagnNextLink"]',)), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        for href in response.xpath('//*[@class="s-result-item  celwidget "]/div/div[2]/div[1]/a/@href'):
            full_url = response.urljoin(href.extract())
            return(scrapy.Request(full_url, callback=self.parse_items))

    def parse_items(self, response):
        items = AmazonItem()
        items['title'] = response.xpath('.//*[@id="productTitle"]/text()').extract()
        items['features'] = response.xpath('.//*[@id="feature-bullets"]/ul//li/span/text()').extract()
        items['product_url'] = response.url
        items['image_urls'] = response.xpath('.//*[@id="landingImage"]/@src').extract()
        return(items)
       
        