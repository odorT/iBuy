from src.extractor.driver import tapaz_driver
import time
from bs4 import BeautifulSoup

PRICE_MAX = 1000000


class Scrape:
    def __init__(self, item, timeout=0.4, min_price=None, max_price=None):
        self.item = item
        self.timeout = timeout
        self.min_price = 0 if min_price is None else min_price
        self.max_price = PRICE_MAX if max_price is None else max_price
        self.driver = tapaz_driver.get_driver()
        self.url = 'https://tap.az/elanlar?&keywords=' + item.replace(' ', '+')
        self.clean_url = 'https://tap.az/'
        self.product_api = {'data': []}

    def source_page_generator(self):
        self.driver.get(self.url)

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
                    price_full = link.find('span', class_='price-val').text + link.find('span', class_='price-cur').text
                except:
                    base_url = None
                    title = None
                    price_full = None

                try:
                    price_full = price_full.replace(',', '.')
                finally:
                    price_full = price_full.replace(' ', '')

                price = float(price_full.split('AZN')[0])
                if price < self.min_price or price > self.max_price:
                    continue

                self.product_api['data'].append({
                    'title': title,
                    'price': price_full,
                    'url': base_url,
                    'rating': None,
                    'short_url': 'www.tap.az'
                })

        time_end = time.time()

        self.product_api.update({
            'details': {
                'exec_time': round((time_end - time_start), 2),
                'total_num': len(self.product_api['data'])
            }
        })

        return self.product_api

    def driver_close(self):
        self.driver.close()
        self.driver.quit()

    def printer(self):
        for i in self.product_api['data']:
            print(f'Title : {i["title"]}, price : {i["price"]}')
        print(self.product_api['details']['exec_time'])

    def run(self):
        self.api_generator()
        self.printer()
