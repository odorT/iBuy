from src.extractor.scraper_tapaz import Scrape_tapaz
from src.extractor.scraper_amazon import Scrape_amazon
from src.extractor.scraper_aliexpress import Scrape_aliexpress
import time


class Distributor:
    def __init__(self, websites, mode, item, timeout, min_price, max_price, sort_price_option,
                 sort_rating_option, currency):
        self.websites = websites
        self.possible_websites = {'tapaz': Scrape_tapaz, 'amazon': Scrape_amazon, 'aliexpress': Scrape_aliexpress}
        self.full_api = {'tapaz': {}, 'amazon': {}, 'aliexpress': {}}
        total_product_num = 0

        time_start = time.time()

        for website, iterscraper in self.possible_websites.items():
            if website in self.websites:
                self.scraper = iterscraper(mode=mode, item=item, timeout=timeout, min_price=min_price,
                                           max_price=max_price, sort_price_option=sort_price_option,
                                           currency=currency,
                                           sort_rating_option=sort_rating_option)
                intermediate_api = self.scraper.get_api()
                self.full_api[website] = intermediate_api
                total_product_num += intermediate_api['details']['total_num']

        time_end = time.time()

        self.full_api.update({
            'details': {
                'exec_time': round(time_end - time_start, 2),
                'total_num': total_product_num
            }
        })

    def get_apis(self):
        return self.full_api
