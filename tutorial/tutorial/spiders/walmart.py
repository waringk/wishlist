

from urllib.parse import urlencode
import scrapy
from home import spider_spawner

import environ

env = environ.Env()
environ.Env.read_env()


API = env('API_KEY')



def get_url(url):
    """Get the API Key and retail URL for web scraping."""
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class WalmartSpider(scrapy.Spider):
    """Create a scraping bot for scraping Walmart.com."""
    name = 'walmart'
    last_return = None
    query_text = None
    result = None

    def start_requests(self):
        """Sends a request with a query text to the scraper to search for on Walmart.com, and then creates the URL
        for the result."""
        queryTextToUse = spider_spawner.qt
        queries = [queryTextToUse]
        for query in queries:
            url = 'https://www.walmart.com/search?' + urlencode({'q': query})
            result = scrapy.Request(url=get_url(url), callback=self.parse_keyword_response)
            yield result

    def parse_keyword_response(self, response):
        """Extracts the product identification number and information for a Walmart product from Walmart.com website
        being scraped."""
        products = response.xpath('//*[@data-item-id]')
        counter = 0
        for product in products:
            pid = product.xpath('@data-item-id').extract_first()
            if pid == "country_cod":
                continue
            if counter == 1:
                break
            product_url = f"https://www.walmart.com/ip/{pid}"
            value = scrapy.Request(url=get_url(product_url), callback=self.parse_product_page, meta={'pid': pid})
            counter += 1
            yield value

    def parse_product_page(self, response):
        """Extracts the product information from the product page where the product is being scraped on Walmart.com"""
        pid = response.meta['pid']
        title = response.xpath('//*[@class="f3 b lh-copy dark-gray mt1 mb2"]/text()').extract_first()
        image = response.xpath('string(//*[@class="mr3 ml7 self-center relative"][1]/*[1]/*[1]/@src)').extract_first()
        price = response.xpath('(//*[@itemprop="price"])[1]/text()').extract_first()

        store = "Walmart"
        self.last_return = {'asin': pid, 'Title': title, 'Price': price, 'MainImage': image, 'Store': store}
        if self.last_return['Title'] != '' and self.last_return['Title'] is not None:
            spider_spawner.test.append(self.last_return)
            self.result = self.last_return
            print("Found Item")
            exit(0)
        yield self.last_return
