
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ImdbCrawler(CrawlSpider):
    name = 'rj'
    allowed_domains = ['www.renegadejuggling.com']
    start_urls = ['https://www.renegadejuggling.com/']
    # rules =(Rule(LinkExtractor()),)
    rules =(Rule(LinkExtractor(),callback='parse_item', follow=True),)
    def parse_item(self, response):
        body_class = response.css("body::attr(class)").get()
        if body_class == "product":
            sku = response.xpath('//*[@id="content"]').re(r'Catalog Number:</span>(.*)</p')[0]
            title = response.xpath('/html/body/section/div[1]/div[1]/h1').re(r'>(.*)<')[0]
            yield {"url": response.url, "body_class": body_class, "title": title, "sku":sku}
        elif body_class is not None:
            yield {"MESSAGE":"NOT PRODUCT","url": response.url, "body_class": body_class}

