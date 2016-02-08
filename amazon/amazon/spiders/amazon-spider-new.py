import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from amazon.items import AmazonItem

class DmozSpider(CrawlSpider):
    name = "amazon"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["http://www.amazon.com/s/ref=sr_1_1_hso_sc_smartcategory_2?rh=n%3A2407749011%2Ck%3Amobile+phones&keywords=mobile+phones&ie=UTF8&qid=1454843899&sr=8-1-acs"
    ]
    
    rules = (
        Rule(scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor(allow=(), restrict_xpaths=('//a[@id="pagnNextLink"]',)), callback='parse_page', follow=True),
    )
    
    
    def parse_items(self, response):
        yield{
            title: response.xpath('//*[@class="s-result-item  celwidget "]/div/div[2]/div[1]/a/span/text()')
        }
       
        