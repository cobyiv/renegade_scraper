
#Imports
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

#Scrapy Crawl Class
#reference: https://docs.scrapy.org/en/latest/topics/spiders.html

class RjCrawler(CrawlSpider):
    '''This is a web crawler specifically designed for the renegade juggling website to find product pages and parse there there html data to find various information that can be exported to a json file'''
    name = 'rj'
    allowed_domains = ['www.renegadejuggling.com']
    start_urls = ['https://www.renegadejuggling.com/']
    rules =(Rule(LinkExtractor(),callback='parse_item', follow=True),)

    def parse_item(self, response):
        '''this function is designed to locate and extract various pieces of information within Renegade Juggling webpages'''
        
        #Determine if the given page is a 'Product' or 'Category' or some other type of website class. Only 'Product' pages will be used downstream
        body_class = response.css("body::attr(class)").get()

        if body_class == "product":

            #Category is found in the html meta property called og:title, example is: "juggling ball | stage ball | renegade juggling"
            categories = response.xpath('/html/head/title').re(r'title>(.*)</title')[0]

            #sku is found on each page as the "Catalog Number"
            sku = response.xpath('//*[@id="content"]').re(r'Catalog Number:</span>(.*)</p')[0]

            #title is the header found at the top of each product page in the big gray letters, in html it is contained in the <h1 class="heading"> tag
            title = response.xpath('/html/body/section/div[1]/div[1]/h1').re(r'>(.*)<')[0]

            #options refer to the main dropdown on each product page, in html this information is contained in the <select class="required" name="option[159][189]" required=""> tag
            options = response.xpath('//*[@id="product_detail_form"]/div[3]/fieldset/div/select').re('<option value=.*>(.*)</option>')

            if len(options) > 0:
                for option in options:
                    yield {"Title": title, "SKU":sku, "Item":option, "Categories":categories}
            else:
                #product_detail_query searchs for items that are in stock or have limited stock if there is no 'options'
                try:
                    product_detail_query = response.xpath('/html/body/section/div[1]/div[3]').re(r'>(.*STOCK.?|.*stock.?|.*Stock.?)<')[0]
                except IndexError:
                    product_detail_query = []
                if len(product_detail_query) > 0:
                    yield {"Title": title, "SKU":sku, "Item":product_detail_query, "Categories":categories}
                else:
                    yield {"Title": title, "SKU":sku, "Item":title, "Categories":categories}
                    
        #if the page is not a 'product page' nothing is outputted.            
        elif body_class is not None:
            pass

