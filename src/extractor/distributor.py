from src.extractor.scraper_tapaz import Scrape_tapaz
from src.extractor.scraper_amazon import Scrape_amazon


# from src.extractor.scraper_amazon import Scrape_aliexpress


class Distributor:
    def __init__(self, websites, mode, item, timeout, min_price, max_price, sort_option, currency):
        self.websites = websites
        self.full_api = {'data': [], 'details': {}}

        if 'tapaz' in self.websites:
            self.scraper1 = Scrape_tapaz(mode=mode, item=item, timeout=timeout, min_price=min_price,
                                         max_price=max_price,
                                         sort_option=sort_option, currency=currency)
            tapaz_api = self.scraper1.get_api()
            self.full_api['data'] += tapaz_api['data']
            self.full_api['details'] = tapaz_api['details']

        # if 'amazon' in self.websites:
        #     self.scraper2 = Scrape_amazon(mode=mode, item=item, timeout=timeout, min_price=min_price,
        #                                   max_price=max_price,
        #                                   sort_option=sort_option, currency=currency)
        #     amazon_api = self.scraper2.api_generator()
        #     self.full_api['data'] += amazon_api['data']

    def get_apis(self):
        return self.full_api
