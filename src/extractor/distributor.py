from src.extractor.option_handler import OptionHandlerInterface, OptionHandler, Sort, Filter
from src.extractor.scrape import AbstractScraper, Scrape_aliexpress, Scrape_tapaz, Scrape_amazon
from src.extractor.driver import Driver
import time


webdriver = Driver(False)

amazon_scraper: AbstractScraper = Scrape_amazon(driver=webdriver)
tapaz_scraper: AbstractScraper = Scrape_tapaz(driver=webdriver, timeout=0.4)
aliexpress_scraper: AbstractScraper = Scrape_aliexpress()

sorter: OptionHandlerInterface = Sort()
filterer: OptionHandlerInterface = Filter()


class Distributor:
    def __init__(self):
        self._scraper_aliexpress = aliexpress_scraper
        self._scraper_amazon = amazon_scraper
        self._scraper_tapaz = tapaz_scraper
        self._sorter = sorter
        self._filterer = filterer

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

                self._sorter.define_options(sort_price_option='ascending', sort_rating_option='default')
                self._filterer.define_options(currency='AZN', min_price=12, max_price=1200)

                handler: OptionHandler = OptionHandler(sort_handler=self._sorter, filter_handler=self._filterer)
                handled = handler.operation(scraped_data)

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
