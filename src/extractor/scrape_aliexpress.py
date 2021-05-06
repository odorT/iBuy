import json
import os
import requests
import time
from os.path import join, dirname
from dotenv import load_dotenv
from src.extractor.scrape import AbstractScraper

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


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
