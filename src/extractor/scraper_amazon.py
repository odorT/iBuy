from src.extractor.driver import amazon_driver
import time
from bs4 import BeautifulSoup

PRICE_MAX = 10000000000

AZN_TO_USD = 0.59
RUB_TO_USD = 0.013
USD_TO_AZN = 1.70
RUB_TO_AZN = 0.022
USD_TO_RUB = 76.08
AZN_TO_RUB = 44.75


class Scrape_amazon:
    def __init__(self, item, timeout=0.4, mode='fast', min_price=None, max_price=None, sort_option=None, currency=None):
        self.item = item
        self.timeout = timeout
        self.mode = mode
        self.min_price = 0 if min_price is None else min_price
        self.max_price = PRICE_MAX if max_price is None else max_price
        self.sort_option = None if sort_option == 'default' else sort_option
        self.currency = None if currency is None else currency
        self.driver = amazon_driver.get_driver()
        self.url = 'https://www.amazon.com/s?k=' + item.replace(' ', '+')
        self.clean_url = 'https://www.amazon.com'
        self.product_api = {'data': []}

    def api_generator(self):
        product = self.item
        if product == '':
            return []
        url = f'https://amazon.com/s?k={product}'

        self.driver.get(url)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        def scrapeInfo(item):
            try:
                atag = item.h2.a
                title = atag.text.strip()
                link = 'https://amazon.com' + atag.get('href')
            except AttributeError:
                title = "No title provided"
            try:
                price_parent = item.find('span', 'a-price')
                price = price_parent.find('span', 'a-offscreen').text.strip()
                price = float(price[1:].replace(',', ''))
            except AttributeError:
                price = 0
            try:
                rating = item.i.text
            except AttributeError:
                rating = "No rating provided"

            product_data = {
                'title': title,
                'price_val': price,
                'rating': rating,
                'url': link,
                'short_url': 'www.amazon.com'
            }

            return product_data

        for item in results:
            record = scrapeInfo(item)
            if record:
                self.product_api['data'].append(record)

        return self.product_api
