
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()

class ImdbCrawler(CrawlSpider):
    name = 'rj'
    allowed_domains = ['www.renegadejuggling.com']
    start_urls = ['https://www.renegadejuggling.com/']
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@class="product"]')),
    )
    # Rule(LinkExtractor(restrict_xpaths='//*[@class="product"]')),
    # Rule(LinkExtractor()),
    
    def parse(self, response):
        # Extract the product name and price from the page
        name = response.xpath('//h1[@class="heading"]/text()').get()
        price = response.xpath('//span[@id="subtotalPrice"]/text()').get()
    
        # Create an item object to store the extracted data
        item = ProductItem()
        item['name'] = name
        item['price'] = price
    
        # Return the item to the Scrapy engine
        yield item