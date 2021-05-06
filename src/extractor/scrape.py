import abc
import json
import os
import requests
from os.path import join, dirname
from dotenv import load_dotenv
import time
from bs4 import BeautifulSoup


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class AbstractScraper(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _get_data(self, *args, **kwargs):
        """
        method returns either a page source or json file full of information about the searched item
        :param *args: page_count
        """
        pass

    @abc.abstractmethod
    def _extract_data(self, page_data):
        """
        this method generates an api from searched item. No filtering is applied here
        :param page_data: page source(str) or json file
        :return: dict
        """
        pass

    @abc.abstractmethod
    def _get_api(self):
        """
        with this method you get the api
        :return: dict
        """
        pass

    @abc.abstractmethod
    def __call__(self, **kwargs):
        """
        Will return scraped data in api form when called
        :param kwargs: search item and etc.
        :return: dict(api)
        """
        pass

    @staticmethod
    def _construct_api(**kwargs):
        """
        this method constructs one standard api structure with python dictionary for all child scraper classes.
        :param kwargs: api data value parameters
        :return: dict
        """
        return {
            'title': kwargs['title'],
            'price_val': kwargs['price_value'],
            'price_curr': kwargs['price_curr'],
            'url': kwargs['base_url'],
            'rating_val': kwargs['rating_val'],
            'rating_over': kwargs['rating_over'],
            'rating': kwargs['rating'],
            'shipping': kwargs['shipping'],
            'short_url': kwargs['short_url']
        }

    @staticmethod
    def _update_details(api, time_start, time_end):
        """
        this method is used to update the api dict with details of:
        execution_time: time passed when getting data from website and constructing api
        total_num: total number of found products
        :param api: api data value parameters
        :param time_start: float
        :param time_end: float
        :return: dict
        """
        api.update({
            'details': {
                'exec_time': round((time_end - time_start), 2),
                'total_num': len(api['data'])
            }
        })
        return api

    @staticmethod
    def _price_formatter(price_value):
        """
        this method cleans the price_value and returns pure float number
        :param price_value: string
        :return: float
        """
        if ' ' in price_value:
            price_value = str(price_value).replace(' ', '')
        if ',' in price_value:
            price_value = price_value.replace(',', '')
        if '$' in price_value:
            price_value = price_value.replace('$', '')
        return float(price_value)

    @staticmethod
    def _printer(api):
        """
        this method prints 3 core parameters of scraped data. Use this method when debugging
        :param api: dict
        """
        for i in api['data']:
            print(f'Title: {i["title"]}')
            print(f'Price: {i["price_val"]}')
            print(f'Rating: {i["rating"]}')
            print('\n\n')


class Scrape_aliexpress(AbstractScraper):
    def __init__(self):
        self.short_url = 'www.aliexpress.com'
        self._product_api = {}

    def _get_data(self, *args):
        global time_start
        time_start = time.time()
        api_source = "https://magic-aliexpress1.p.rapidapi.com/api/products/search"

        querystring = {"name": self.item, "page": "1"}

        headers = {
            'x-rapidapi-key': os.environ.get("X_RAPIDAPI_KEY"),
            'x-rapidapi-host': os.environ.get("X_RAPIDAPI_HOST_500_MO")
        }

        response = requests.request("GET", api_source, headers=headers, params=querystring)

        # with open("json_responses.txt", "a") as json_file:
        #     json_file.write(str(response.text))
        #     json_file.write('\nNew request\n')

        return json.loads(str(response.text))

    def _extract_data(self, response):
        item_list = response['docs']
        api = {'data': []}

        rating_over = '5'

        for item in item_list:
            title = item['product_title']
            price_value = item['app_sale_price']
            price_curr = item['app_sale_price_currency']
            base_url = item['product_detail_url']

            try:
                shipping = item['metadata']['logistics']['logisticsDesc']
                rating_val = item['evaluate_rate']
                rating = str(rating_val) + '/5'
            except:
                shipping = None
                rating_val = 0
                rating = None

            api['data'].append(
                self._construct_api(title=title, price_value=price_value, price_curr=price_curr, base_url=base_url,
                                    rating_val=rating_val, rating_over=rating_over, rating=rating, shipping=shipping,
                                    short_url=self.short_url))
        time_end = time.time()
        self._update_details(api, time_start=time_start, time_end=time_end)

        return api

    def _get_api(self):
        json_data = self._get_data()
        return self._extract_data(json_data)

    def __call__(self, **kwargs):
        self.item = kwargs['item']
        self._product_api = self._get_api()

        return self._product_api


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
        page_data = self._get_data(1)
        soup = BeautifulSoup(page_data, 'lxml')
        page_count = self.find_page_count(soup)
        time_start = time.time()

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


class Scrape_tapaz(AbstractScraper):
    def __init__(self, driver, timeout=0.4):
        self.timeout = timeout
        self.driver = driver.get_driver()
        self.short_url = 'www.tap.az'
        self._product_api = {}

    def _get_data(self, *args):
        global time_start
        time_start = time.time()

        self.driver.get(self.url)

        if self.mode == '1':
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.timeout)
        elif self.mode == '2':
            for _ in range(10):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.timeout)
        elif self.mode == '3':
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

    def _extract_data(self, page_data):
        final_page = page_data
        start_string = '<div class="js-endless-container products endless-products">'
        end_string = '<div class="pagination_loading">'
        main_html = str(final_page)[str(final_page).find(start_string):]
        main_html = main_html[:main_html.find(end_string)]

        soup = BeautifulSoup(main_html, 'lxml')
        product_list = soup.select("div[class^=products-i]")
        api = {'data': []}

        rating_val = '0'
        rating_over = '5'
        rating = None
        shipping = None

        for item in product_list:
            for link in item.find_all('a', target='_blank', href=True):
                try:
                    base_url = 'https://tap.az/' + link['href']
                    title = link.find('div', class_='products-name').text
                    price_value = self._price_formatter(link.find('span', class_='price-val').text)
                    price_curr = link.find('span', class_='price-cur').text
                except:
                    continue

                api['data'].append(
                    self._construct_api(title=title, price_value=price_value, price_curr=price_curr, base_url=base_url,
                                        rating_val=rating_val, rating_over=rating_over, rating=rating,
                                        shipping=shipping, short_url=self.short_url))

        time_end = time.time()
        self._update_details(api, time_start=time_start, time_end=time_end)

        return api

    def _get_api(self):
        page_data = self._get_data()
        return self._extract_data(page_data=page_data)

    def __call__(self, **kwargs):
        self.item = kwargs['item']
        self.mode = kwargs['mode']
        self.url = 'https://tap.az/elanlar?&keywords=' + self.item.replace(' ', '+')
        self._product_api = self._get_api()

        return self._product_api
