from src.extractor.scrape import AbstractScraper
import time
from bs4 import BeautifulSoup


class Scrape_amazon(AbstractScraper):
    def __init__(self, driver):
        self.driver = driver.get_driver()
        self.short_url = 'www.amazon.com'
        self._product_api = {}

    def _get_data(self, *args):
        self.driver.get(self.url + "&page=" + str(args[0]))

        return self.driver.page_source

    @staticmethod
    def find_page_count(soup):
        page_count = 1
        try:
            page_count_area = soup.find_all("ul", class_="a-pagination")
            for i in page_count_area:
                number_area = i.text.strip()
            page_count_nums = list(str(number_area).split('\n'))

            for i in page_count_nums:
                try:
                    if int(i) > page_count:
                        page_count = int(i)
                except:
                    continue
        except:
            pass

        return page_count

    def _extract_data(self, soup):
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

        return api

    def _get_api(self):
        time_start = time.time()
        page_data = self._get_data(1)
        soup = BeautifulSoup(page_data, 'lxml')
        page_count = self.find_page_count(soup)

        if self.mode == '1' or page_count == 1:
            temp_api = self._extract_data(soup)

            time_end = time.time()
            self._update_details(temp_api, time_start=time_start, time_end=time_end)
            return temp_api

        elif self.mode == '2':
            temp_api = {'data': []}
            for i in range(1, 6):
                page_data = self._get_data(i)
                soup = BeautifulSoup(page_data, 'lxml')
                temp_api['data'].extend(self._extract_data(soup)['data'])

            time_end = time.time()
            self._update_details(temp_api, time_start=time_start, time_end=time_end)
            return temp_api

        elif self.mode == '3':
            temp_api = {'data': []}
            for i in range(1, page_count):
                page_data = self._get_data(i)
                soup = BeautifulSoup(page_data, 'lxml')
                temp_api['data'].extend(self._extract_data(soup)['data'])

            time_end = time.time()
            self._update_details(temp_api, time_start=time_start, time_end=time_end)
            return temp_api

    def __call__(self, **kwargs):
        self.item = kwargs['item']
        self.mode = kwargs['mode']
        self.url = 'https://www.amazon.com/s?k=' + self.item
        self._product_api = self._get_api()

        return self._product_api
