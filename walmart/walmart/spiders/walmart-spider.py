import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

class walmartSpider(CrawlSpider):
    name = "walmart"
    allowed_domains = ["www.walmart.com"]
    start_urls = ["http://www.walmart.com/search/?query=mobile%20phones&cat_id=3944_542371_1073085"
    ]
    
    rules = (
        Rule(scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor(allow=(), restrict_xpaths=('//*[@id="paginator-container"]/div/a',)), callback='parse_page', follow=True),
    )
    
    
    def parse_items(self, response):
        yield{
            'title': response #TODO
        }
       
        