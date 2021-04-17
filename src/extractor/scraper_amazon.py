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
        self.currency = None if currency == 'default' is None else currency
        self.driver = amazon_driver.get_driver()
        self.url = 'https://www.amazon.com/s?k=' + self.item
        self.clean_url = 'https://www.amazon.com'
        self.product_api = {'data': []}

    @staticmethod
    def price_formatter(price_value):
        if ' ' in price_value:
            price_value = str(price_value).replace(' ', '')
        if ',' in price_value:
            price_value = price_value.replace(',', '')
        if '$' in price_value:
            price_value = price_value.replace('$', '')
        return float(price_value)

    def with_currency(self, api):
        for data in api['data']:
            if self.currency == 'usd':
                if data['price_curr'] == 'AZN':
                    data['price_val'] = round(data['price_val'] * AZN_TO_USD, 2)
                elif data['price_curr'] == 'RUB':
                    data['price_val'] = round(data['price_val'] * RUB_TO_USD, 2)
                data['price_curr'] = 'USD'
            elif self.currency == 'azn':
                print(data['price_curr'])
                print(data['price_val'])
                if data['price_curr'] == 'USD':
                    data['price_val'] = round(data['price_val'] * USD_TO_AZN, 2)
                elif data['price_curr'] == 'RUB':
                    data['price_val'] = round(data['price_val'] * RUB_TO_AZN, 2)
                data['price_curr'] = 'AZN'
            elif self.currency == 'rub':
                if data['price_curr'] == 'USD':
                    data['price_val'] = round(data['price_val'] * USD_TO_RUB, 2)
                elif data['price_curr'] == 'AZN':
                    data['price_val'] = round(data['price_val'] * AZN_TO_RUB, 2)
                data['price_curr'] = 'RUB'

        return api

    def with_price_limits(self, api):
        api['data'] = filter(lambda x: self.max_price > x['price_val'] >= self.min_price, api['data'])
        # api['data'] = [x for x in api['data'] if self.max_price > x['price_val'] > self.min_price]
        return api

    def with_sort_options(self, api):
        api['data'] = sorted(api['data'], key=lambda x: x['price_val'], reverse=(self.sort_option == 'descending'))
        return api

    def source_page_generator(self):
        # if self.mode == 'fast':
        #     for page in range(4):
        #         url = self.url + '&page=' + str(page)
        pass

    def api_generator(self):
        time_start = time.time()

        self.driver.get(self.url)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            try:
                title = item.find('span', class_='a-size-medium a-color-base a-text-normal').text
                base_url = self.clean_url + item.find('a', class_='a-link-normal a-text-normal')['href']
                price_val = self.price_formatter(item.find('span', class_='a-offscreen').text)
                price_curr = 'USD'
            except:
                continue
            try:
                rating = item.find('span', class_='a-icon-alt').text
                rating_val = float(str(rating).replace(' out of ', '/').replace(' stars', '').replace('/5', ''))
                rating_over = str(rating).replace(' out of ', '/').replace(' stars', '').split('/')[1]
                rating = str(rating_val) + '/' + rating_over
            except:
                rating_val = None
                rating_over = None
                rating = None

            self.product_api['data'].append({
                'title': title,
                'price_val': price_val,
                'price_curr': price_curr,
                'url': base_url,
                'rating_val': rating_val,
                'rating_over': rating_over,
                'rating': rating,
                'short_url': 'www.amazon.com'
            })

        time_end = time.time()

        self.product_api.update({
            'details': {
                'exec_time': round((time_end - time_start), 2),
                'total_num': len(self.product_api['data'])
            }
        })

        return self.product_api

    def get_api(self):
        api = self.api_generator()

        if self.currency:
            api = self.with_currency(api)
        if self.min_price != 0 or self.max_price != PRICE_MAX:
            api = self.with_price_limits(api)
        if self.sort_option:
            api = self.with_sort_options(api)

        return api

    def printer(self):
        for i in self.product_api['data']:
            print(f'Title: {i["title"]}')
            print(f'Price: {i["price_val"]}')
            print(f'Rating: {i["rating"]}')
            print('\n\n')
        print(self.product_api)

    def driver_close(self):
        self.driver.stop_driver()

    def run(self):
        self.api_generator()
        self.printer()

