from src.extractor.driver import amazon_driver
from src.extractor.scrape import Scraper
import time
from bs4 import BeautifulSoup


class Scrape_amazon(Scraper):
    def __init__(self, **kwargs):
        self.item = kwargs['item']
        self.driver = amazon_driver.get_driver()
        self.url = 'https://www.amazon.com/s?k=' + self.item
        self.short_url = 'www.amazon.com'
        self.product_api = {}

    def get_data(self):
        global time_start
        time_start = time.time()  # for calculating the overall execution time of scraping

        self.driver.get(self.url)

        return self.driver.page_source

    def extract_data(self, page_data):
        soup = BeautifulSoup(page_data, 'lxml')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        api = {'data': []}

        shipping = None

        for item in results:
            try:
                title = item.find('span', class_='a-size-medium a-color-base a-text-normal').text
                base_url = 'https://www.amazon.com' + item.find('a', class_='a-link-normal a-text-normal')['href']
                price_value = self.price_formatter(item.find('span', class_='a-offscreen').text)
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

            api['data'].append(self.construct_api(title=title, price_value=price_value, price_curr=price_curr,
                                                  base_url=base_url, rating_val=rating_val, rating_over=rating_over,
                                                  rating=rating, shipping=shipping, short_url=self.short_url))
        time_end = time.time()
        self.update_details(api, time_start=time_start, time_end=time_end)

        return api

    def get_api(self):
        page_data = self.get_data()
        self.product_api = self.extract_data(page_data=page_data)

        return self.product_api
