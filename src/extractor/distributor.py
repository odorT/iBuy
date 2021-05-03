from src.extractor.option_handler import OptionHandlerInterface, OptionHandler, Sort, Filter
from src.extractor.scrape import AbstractScraper, Scrape_aliexpress, Scrape_tapaz, Scrape_amazon
from src.extractor.driver import Driver
import time

webdriver = Driver(headless=True)

amazon_scraper = Scrape_amazon(driver=webdriver)
tapaz_scraper = Scrape_tapaz(driver=webdriver, timeout=0.4)
aliexpress_scraper = Scrape_aliexpress()

sorter = Sort()
filterer = Filter()


class DistributorOptions(object):
    def __init__(self):
        self._arguments = []
        self._possible_arguments = ['tapaz', 'amazon', 'aliexpress']

    def add_argument(self, argument):  # sourcery skip: remove-redundant-if
        """
        Adds an argument to the list

        :Args:
         - Sets the arguments
        """
        if argument in self._possible_arguments:
            self._arguments.append(argument)
        elif argument not in self._possible_arguments:
            raise ValueError("no such argument")
        else:
            raise ValueError("argument can not be null")

    @property
    def arguments(self):
        """
        Returns a list of arguments needed for the distributor
        """
        return self._arguments


class Distributor:
    __filterer: OptionHandlerInterface
    __sorter: OptionHandlerInterface
    __scraper_aliexpress: AbstractScraper
    __scraper_amazon: AbstractScraper
    __scraper_tapaz: AbstractScraper

    def __init__(self, options: DistributorOptions = None):
        self.__sorter = sorter
        self.__filterer = filterer

        if options:
            self.__argument_wrapper(options)
        else:
            self.__argument_wrapper()
        self.__full_api = {'tapaz': {}, 'amazon': {}, 'aliexpress': {}}

    def __argument_wrapper(self, options=None):
        if options:
            self.__possible_websites = {}

            if 'tapaz' in options.arguments:
                self.__scraper_tapaz = tapaz_scraper
                self.__possible_websites.update({'tapaz': self.__scraper_tapaz})

            if 'amazon' in options.arguments:
                self.__scraper_amazon = amazon_scraper
                self.__possible_websites.update({'amazon': self.__scraper_amazon})

            if 'aliexpress' in options.arguments:
                self.__scraper_aliexpress = aliexpress_scraper
                self.__possible_websites.update({'aliexpress': self.__scraper_aliexpress})

        else:
            self.__scraper_tapaz = tapaz_scraper
            self.__scraper_amazon = amazon_scraper
            self.__scraper_aliexpress = aliexpress_scraper

            self.__possible_websites = {'tapaz': self.__scraper_tapaz, 'amazon': self.__scraper_amazon,
                                        'aliexpress': self.__scraper_aliexpress}

    def __call__(self, **kwargs):
        self.__websites: list = kwargs['websites']
        time_start = time.time()
        total_product_num = 0

        for website, iterscraper in self.__possible_websites.items():
            if website in self.__websites:
                scraped_data = iterscraper(item=kwargs['item'], mode=kwargs['mode'])

                self.__sorter.define_options(sort_price_option='ascending', sort_rating_option='default')
                self.__filterer.define_options(currency='AZN', min_price=12, max_price=1200)

                handler: OptionHandler = OptionHandler(sort_handler=self.__sorter, filter_handler=self.__filterer)
                handled = handler.operation(scraped_data)

                self.__full_api.update({website: handled})
                total_product_num += handled['details']['total_num']

        time_end = time.time()

        self.__full_api.update({
            'details': {
                'exec_time': round(time_end - time_start, 2),
                'total_num': total_product_num
            }
        })

        print(f'GET request: {kwargs}\nRESPONSE: {self.__full_api}')

        return self.__full_api
