import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class RJ(CrawlSpider):
    name = "av_rj"
    allowed_domains = ['www.renegadejuggling.com']
    start_urls = ['https://www.renegadejuggling.com']
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@class="Product"]'), callback='parse_item'),
        Rule(LinkExtractor()),
    )


    def parse_item(self, response):
        try:
            yield{ 
                'name': response.css('h1.heading::text').get(),
                'price': response.css('span#subtotalPrice').attrib['data-price']
            }
        except:
            yield{ 
                'name': "-no name-",
                'price': "-no price-"
            }

    # def parse_item2(self, response):
    #     yield{ 
    #         'name': "-skipped-",
    #         'price': "-skipped-"
    #     }