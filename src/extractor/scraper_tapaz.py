from src.extractor.driver import Driver
from src.extractor.scraper import Scraper
import time
from bs4 import BeautifulSoup


class Scrape_tapaz(Scraper):
    def __init__(self, item, mode='fast', timeout=0.4, min_price=None, max_price=None,
                 sort_option=None, currency=None, headless=True):
        super(Scrape_tapaz, self).__init__(currency, min_price, max_price, sort_option)
        self.item = item
        self.timeout = timeout
        self.mode = mode
        self.driver = Driver(headless=headless).get_driver()
        self.url = 'https://tap.az/elanlar?&keywords=' + item.replace(' ', '+')
        self.clean_url = 'https://tap.az/'
        self.product_api = {}

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
        api = {'data': []}

        for item in product_list:
            for link in item.find_all('a', target='_blank', href=True):
                try:
                    base_url = self.clean_url + link['href']
                    title = link.find('div', class_='products-name').text
                    price_value = self.price_formatter(link.find('span', class_='price-val').text)
                    price_curr = link.find('span', class_='price-cur').text

                    api['data'].append({
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

        api.update({
            'details': {
                'exec_time': round((time_end - time_start), 2),
                'total_num': len(api['data'])
            }
        })

        return api

    def get_api(self):
        api = self.api_generator()
        self.product_api = self.with_options(api)

        return self.product_api

    def run(self):
        api = self.get_api()
        self.printer(api)
