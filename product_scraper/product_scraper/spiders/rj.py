
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
            options = response.xpath('//*[@id="product_detail_form"]/div[3]/fieldset/div/select').re('<option value=.*>(.*)</option>')
            if len(options) > 0:
                for option in options:
                    yield {"title": title, "sku":sku, "item":option}
            else:
                yield {"title": title, "sku":sku, "item":title}
        elif body_class is not None:
            pass
            # yield {"MESSAGE":"NOT PRODUCT","url": response.url, "body_class": body_class}


# {"url": response.url, "body_class": body_class, "title": title, "sku":sku}

