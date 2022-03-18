# Citation for the code from this file:
# Date: 3/12/2022
# Modified from:
# Source URL: https://www.datasciencecentral.com/how-to-scrape-amazon-product-data/

import re
from urllib.parse import urlencode
import scrapy
from home import spider_spawner

API = '2432af4bc519ab7c1c05de40daef45c3'


def get_url(url):
    """Get the API Key and retail URL for web scraping."""
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class AmazonSpider(scrapy.Spider):
    """Create a scraping bot for scraping Amazon.com."""
    name = 'amazon'
    last_return = None
    query_text = None
    result = None

    def start_requests(self):
        """Sends a request with a query text to the scraper to search for on Amazon.com, and then creates the URL
        for the result."""
        queryTextToUse = spider_spawner.qt
        print("query_text is", queryTextToUse)
        queries = [queryTextToUse]
        for query in queries:
            url = 'https://www.amazon.com/s?' + urlencode({'k': query})
            result = scrapy.Request(url=get_url(url), callback=self.parse_keyword_response)
            print("Result =", result)
            yield result

    def parse_keyword_response(self, response):
        """Extracts the product identification number and information for an Amazon product from Amazon.com website
        being scraped."""
        products = response.xpath('//*[@data-asin]')
        counter = 0
        for product in products:
            asin = response.xpath(
                'string(//*[@class="a-size-base-plus a-color-base a-text-normal"][1]/ancestor::div[@data-asin[not('
                '.="")]]/@data-asin)').extract_first()
            if counter == 1:
                break
            if asin == "country_cod":
                continue
            if asin == '':
                continue
            product_url = f"https://www.amazon.com/dp/{asin}"
            value = scrapy.Request(url=get_url(product_url), callback=self.parse_product_page, meta={'asin': asin})
            counter += 1
            yield value

    def parse_product_page(self, response):
        """Extracts the product information from the product page where the product is being scraped on Amazon.com."""
        asin = response.meta['asin']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        img = re.search('"large":"(.*?)"', response.text)
        image = None
        if img is not None:
            image = img.groups()[0]
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()

        if not price:
            price = response.xpath('//*[@data-asin-price]/@data-asin-price').extract_first() or \
                    response.xpath('//*[@id="price_inside_buybox"]/text()').extract_first()
        if not price:
            price = response.xpath('//*[@class="a-price a-text-price a-size-medium apexPriceToPay"][1]/*[1]/text()'). \
                extract_first()
        if not price:
            price = response.xpath('//*[@class="a-price aok-align-center reinventPricePriceToPayPadding priceToPay"]['
                                   '1]/*[1]/text()').extract_first()
        store = "Amazon"
        self.last_return = {'asin': asin, 'Title': title, 'MainImage': image, 'Price': price, 'Store': store}
        if self.last_return['Title'] != '' and self.last_return['Title'] is not None:
            spider_spawner.test.append(self.last_return)
            self.result = self.last_return
            print("Found Item")
            exit(0)
        yield self.last_return
