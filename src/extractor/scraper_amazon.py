from src.extractor.driver import amazon_driver
from src.extractor.scrape import Scraper
import time
from bs4 import BeautifulSoup


class Scrape_amazon(Scraper):
    def __init__(self):
        self.driver = amazon_driver.get_driver()
        self.short_url = 'www.amazon.com'
        self._product_api = {}

    def __call__(self, **kwargs):
        self.item = kwargs['item']
        self.url = 'https://www.amazon.com/s?k=' + self.item

    def _get_data(self):
        global time_start
        time_start = time.time()  # for calculating the overall execution time of scraping

        self.driver.get(self.url)

        return self.driver.page_source

    def _extract_data(self, page_data):
        soup = BeautifulSoup(page_data, 'lxml')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        api = {'data': []}

        shipping = None

        for item in results:
            try:
                title = item.find('span', class_='a-size-medium a-color-base a-text-normal').text
                base_url = 'https://www.amazon.com' + item.find('a', class_='a-link-normal a-text-normal')['href']
                price_value = self._price_formatter(item.find('span', class_='a-offscreen').text)
                price_curr = 'USD'
            except:
                continue
            try:
                rating = item.find('span', class_='a-icon-alt').text
                rating_val = float(str(rating).replace(' out of ', '/').replace(' stars', '').replace('/5', ''))
                rating_over = str(rating).replace(' out of ', '/').replace(' stars', '').split('/')[1]
                rating = str(rating_val) + '/' + rating_over
            except:
                rating_val = '0'
                rating_over = '5'
                rating = None

            api['data'].append(
                self._construct_api(title=title, price_value=price_value, price_curr=price_curr, base_url=base_url,
                                    rating_val=rating_val, rating_over=rating_over, rating=rating, shipping=shipping,
                                    short_url=self.short_url))
        time_end = time.time()
        self._update_details(api, time_start=time_start, time_end=time_end)

        return api

    def _get_api(self):
        page_data = self._get_data()
        return self._extract_data(page_data=page_data)

    def __call__(self, **kwargs):
        self.item = kwargs['item']
        self.url = 'https://www.amazon.com/s?k=' + self.item
        self._product_api = self._get_api()

        return self._product_api
