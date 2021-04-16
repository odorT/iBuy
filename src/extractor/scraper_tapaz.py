from src.extractor.driver import tapaz_driver
import time
from bs4 import BeautifulSoup

PRICE_MAX = 10000000000

AZN_TO_USD = 0.59
RUB_TO_USD = 0.013
USD_TO_AZN = 1.70
RUB_TO_AZN = 0.022
USD_TO_RUB = 76.08
AZN_TO_RUB = 44.75


class Scrape_tapaz:
    def __init__(self, item, timeout=0.4, mode='fast', min_price=None, max_price=None, sort_option=None, currency=None):
        self.item = item
        self.timeout = timeout
        self.mode = mode
        self.min_price = 0 if min_price is None else min_price
        self.max_price = PRICE_MAX if max_price is None else max_price
        self.sort_option = None if sort_option == 'default' else sort_option
        self.currency = None if currency is None else currency
        self.driver = tapaz_driver.get_driver()
        self.url = 'https://tap.az/elanlar?&keywords=' + item.replace(' ', '+')
        self.clean_url = 'https://tap.az/'
        self.product_api = {'data': []}

    @staticmethod
    def price_formatter(price_value):
        if ' ' in price_value:
            price_value = str(price_value).replace(' ', '')
        if ',' in price_value:
            price_value = price_value.replace(',', '.')
        return float(price_value)

    def with_sort_options(self, api):
        api['data'] = sorted(api['data'], key=lambda x: x['price_val'], reverse=(self.sort_option == 'descending'))
        return api

    def with_price_limits(self, api):
        api['data'] = filter(lambda x: self.max_price > x['price_val'] >= self.min_price, api['data'])
        # api['data'] = [x for x in api['data'] if self.max_price > x['price_val'] > self.min_price]
        return api

    def with_currency(self, api):
        for data in api['data']:
            if self.currency == 'usd':
                if data['price_curr'] == 'AZN':
                    data['price_val'] = round(data['price_val'] * AZN_TO_USD, 2)
                elif data['price_curr'] == 'RUB':
                    data['price_val'] = round(data['price_val'] * RUB_TO_USD, 2)
                data['price_curr'] = 'USD'
            elif self.currency == 'azn':
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

    def source_page_generator(self):
        self.driver.get(self.url)

        if self.mode == 'fast':
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.timeout)
        elif self.mode == 'slow':
            number_of_scrolls = 0
            reached_page_end = False
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while not reached_page_end:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.timeout)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if last_height == new_height:
                    reached_page_end = True
                else:
                    last_height = new_height
                number_of_scrolls += 1

        return self.driver.page_source

    def api_generator(self):
        time_start = time.time()    # to calculate overall execution time

        final_page = self.source_page_generator()
        start_string = '<div class="js-endless-container products endless-products">'
        end_string = '<div class="pagination_loading">'
        main_html = str(final_page)[str(final_page).find(start_string):]
        main_html = main_html[:main_html.find(end_string)]

        soup = BeautifulSoup(main_html, 'lxml')
        product_list = soup.select("div[class^=products-i]")

        for item in product_list:
            for link in item.find_all('a', target='_blank', href=True):
                try:
                    base_url = self.clean_url + link['href']
                    title = link.find('div', class_='products-name').text
                    price_value = self.price_formatter(link.find('span', class_='price-val').text)
                    price_curr = link.find('span', class_='price-cur').text

                    self.product_api['data'].append({
                        'title': title,
                        'price_val': price_value,
                        'price_curr': price_curr,
                        'url': base_url,
                        'rating': None,
                        'short_url': 'www.tap.az'
                    })
                except:
                    continue

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
        print(self.sort_option, self.min_price, self.max_price, self.currency)

        if self.currency:
            api = self.with_currency(api)
        if self.min_price != 0 or self.max_price != PRICE_MAX:
            api = self.with_price_limits(api)
        if self.sort_option:
            api = self.with_sort_options(api)

        return api

    def driver_close(self):
        self.driver.close()
        self.driver.quit()

    def printer(self):
        # for i in self.product_api['data']:
        #     print(f'Title : {i["title"]}, price : {i["price"]}')
        # print(self.product_api['details']['exec_time'])
        print(self.product_api)

    def run(self):
        self.api_generator()
        self.printer()
