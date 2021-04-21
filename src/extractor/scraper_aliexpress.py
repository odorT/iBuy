from src.extractor.driver import Driver
from src.extractor.scraper import Scraper
import time
import json
import requests

aliexpress_scraper = Driver(True)


class Scrape_aliexpress(Scraper):
    def __init__(self, item, min_price=None, max_price=None, sort_price_option=None, sort_rating_option=None,
                 currency=None):
        super(Scrape_aliexpress, self).__init__(currency=currency, min_price=min_price, max_price=max_price,
                                                sort_price_option=sort_price_option,
                                                sort_rating_option=sort_rating_option)
        self.item = item
        self.clean_url = 'https://www.aliexpress.com/item/'
        self.product_api = {}

    def json_response_generator(self):
        url = "https://ali-express1.p.rapidapi.com/search"

        querystring = {"query": self.item, "page": "1"}

        headers = {
            'x-rapidapi-key': "5f68165e2emshf9462f5483ad7bap17785ajsna20dfc08cf3a",
            'x-rapidapi-host': "ali-express1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        with open("json_responses.txt", "a") as json_file:
            json_file.write(str(response.text))
            json_file.write('\nNew request\n')

        return json.loads(str(response.text))

    def api_generator_from_response(self):
        time_start = time.time()

        response = self.json_response_generator()

        item_list = response['data']['searchResult']['mods']['itemList']['content']
        api = {'data': []}

        for item in item_list:
            title = item['title']['displayTitle']
            price_value = item['prices']['sale_price']['minPrice']
            price_curr = item['prices']['sale_price']['currencyCode']
            product_id = item['productId']

            try:
                shipping = item['logistics']['logisticsDesc']
                rating_val = item['evaluation']['starRating']
                rating = str(rating_val) + '/5'
            except:
                shipping = None
                rating_val = None
                rating = None

            api['data'].append({
                'title': title,
                'price_val': price_value,
                'price_curr': price_curr,
                'url': self.clean_url + str(product_id) + '.html',
                'rating_val': rating_val,
                'rating_over': 5,
                'rating': rating,
                'shipping': shipping,
                'short_url': 'www.aliexpress.com'
            })

        time_end = time.time()

        api.update({
            'details': {
                'exec_time': round((time_end - time_start), 2),
                'total_num': len(api['data'])
            }
        })

        print(api)
        return api

    def get_api(self):
        api = self.api_generator_from_response()
        self.product_api = self.with_options(api)

        return self.product_api

    def run(self):
        api = self.get_api()
        self.printer(api)
