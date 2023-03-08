
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ImdbCrawler(CrawlSpider):
    name = 'rj'
    allowed_domains = ['www.renegadejuggling.com']
    start_urls = ['https://www.renegadejuggling.com/']
    rules = (Rule(LinkExtractor()),)