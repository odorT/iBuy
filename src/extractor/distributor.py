from src.extractor.scrape import Scraper
from src.extractor.scraper_tapaz import Scrape_tapaz
from src.extractor.scraper_amazon import Scrape_amazon
from src.extractor.scraper_aliexpress import Scrape_aliexpress
from src.extractor.option_handler import Options
import time


class Distributor:
    def __call__(self, **kwargs):
        self.websites: list = kwargs['websites']
        self.full_api = {'tapaz': {}, 'amazon': {}, 'aliexpress': {}}

        possible_websites = {'tapaz': Scrape_tapaz, 'amazon': Scrape_amazon, 'aliexpress': Scrape_aliexpress}
        total_product_num = 0

        time_start = time.time()

        for website, iterscraper in possible_websites.items():
            if website in self.websites:
                scraper: Scraper = iterscraper(item=kwargs['item'], mode=kwargs['mode'])
                options: Options = Options(currency=kwargs['currency'], min_price=kwargs['min_price'],
                                           max_price=kwargs['max_price'], sort_price_option=kwargs['sort_price_option'],
                                           sort_rating_option=kwargs['sort_rating_option'])

                scraped_data_api = scraper.get_api()
                handled = options.handle(scraped_data_api)

                self.full_api.update({website: handled})
                total_product_num += handled['details']['total_num']

        time_end = time.time()

        self.full_api.update({
            'details': {
                'exec_time': round(time_end - time_start, 2),
                'total_num': total_product_num
            }
        })

        return self.full_api
