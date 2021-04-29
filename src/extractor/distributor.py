from src.extractor.option_handler import OptionHandler
from src.extractor.scraper_tapaz import Scrape_tapaz
from src.extractor.scraper_amazon import Scrape_amazon
from src.extractor.scraper_aliexpress import Scrape_aliexpress
import time


class Distributor:
    def __init__(self):
        self._scraper_aliexpress = Scrape_aliexpress()
        self._scraper_amazon = Scrape_amazon()
        self._scraper_tapaz = Scrape_tapaz()
        self._possible_websites = {'tapaz': self._scraper_tapaz, 'amazon': self._scraper_amazon,
                                   'aliexpress': self._scraper_aliexpress}
        self._full_api = {'tapaz': {}, 'amazon': {}, 'aliexpress': {}}

    def __call__(self, **kwargs):
        self._websites: list = kwargs['websites']
        time_start = time.time()
        total_product_num = 0

        for website, iterscraper in self._possible_websites.items():
            if website in self._websites:
                scraped_data = iterscraper(item=kwargs['item'], mode=kwargs['mode'])
                options: OptionHandler = OptionHandler(currency=kwargs['currency'], min_price=kwargs['min_price'],
                                                       max_price=kwargs['max_price'], sort_price_option=kwargs['sort_price_option'],
                                                       sort_rating_option=kwargs['sort_rating_option'])
                handled = options.handle(scraped_data)

                self._full_api.update({website: handled})
                total_product_num += handled['details']['total_num']

        time_end = time.time()

        self._full_api.update({
            'details': {
                'exec_time': round(time_end - time_start, 2),
                'total_num': total_product_num
            }
        })

        print(f'GET request: {kwargs}\nRESPONSE: {self._full_api}')

        return self._full_api
