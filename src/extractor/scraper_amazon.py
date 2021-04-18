from src.extractor.driver import Driver
from src.extractor.scraper import Scraper
import time
from bs4 import BeautifulSoup


class Scrape_amazon(Scraper):
    def __init__(self, item, timeout=0.4, mode='fast', min_price=None, max_price=None,
                 sort_option=None, currency=None, headless=True):
        super(Scrape_amazon, self).__init__(currency, min_price, max_price, sort_option)
        self.item = item
        self.timeout = timeout
        self.mode = mode
        self.driver = Driver(headless=headless).get_driver()
        self.url = 'https://www.amazon.com/s?k=' + self.item
        self.clean_url = 'https://www.amazon.com'
        self.product_api = {}

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
        api = {'data': []}

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

            api['data'].append({
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
