from src.extractor.scraper_tapaz import Scrape_tapaz
from src.extractor.scraper_amazon import Scrape_amazon
import time

# from src.extractor.scraper_amazon import Scrape_aliexpress


class Distributor:
    def __init__(self, websites, mode, item, timeout, min_price, max_price, sort_price_option,
                 sort_rating_option, currency):
        self.websites = websites
        self.full_api = {'tapaz': {}, 'amazon': {}, 'aliexpress': {}}
        total_product_num = 0

        time_start = time.time()

        if 'tapaz' in self.websites:
            self.scraper1 = Scrape_tapaz(mode=mode, item=item, timeout=timeout, min_price=min_price,
                                         max_price=max_price, sort_price_option=sort_price_option, currency=currency,
                                         sort_rating_option=sort_rating_option)
            tapaz_api = self.scraper1.get_api()
            self.full_api['tapaz'] = tapaz_api
            total_product_num += tapaz_api['details']['total_num']

        if 'amazon' in self.websites:
            self.scraper2 = Scrape_amazon(mode=mode, item=item, timeout=timeout, min_price=min_price,
                                          max_price=max_price, sort_price_option=sort_price_option, currency=currency,
                                          sort_rating_option=sort_rating_option)
            amazon_api = self.scraper2.get_api()
            self.full_api['amazon'] = amazon_api
            total_product_num += amazon_api['details']['total_num']

        time_end = time.time()

        self.full_api.update({
            'details': {
                'exec_time': round(time_end - time_start, 2),
                'total_num': total_product_num
            }
        })

    def get_apis(self):
        return self.full_api
