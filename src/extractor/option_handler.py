
AZN_TO_USD = 0.59
RUB_TO_USD = 0.013
USD_TO_AZN = 1.70
RUB_TO_AZN = 0.022
USD_TO_RUB = 76.08
AZN_TO_RUB = 44.75


class OptionHandler:
    def __init__(self, **kwargs):
        self.PRICE_MAX = 10000000000
        self.currency = None if kwargs['currency'] == 'default' else kwargs['currency']
        self.min_price = 0 if kwargs['min_price'] is None else kwargs['min_price']
        self.max_price = self.PRICE_MAX if kwargs['max_price'] is None else kwargs['max_price']
        self.sort_price_option = None if kwargs['sort_price_option'] == 'default' else kwargs['sort_price_option']
        self.sort_rating_option = None if kwargs['sort_rating_option'] == 'default' else kwargs['sort_rating_option']

    def handle(self, scraper_data):

        if self.currency:
            scraper_data = Filter.with_currency(self, scraper_data)
        if self.min_price != 0 or self.max_price != self.PRICE_MAX:
            scraper_data = Filter.with_price_limits(self, scraper_data)
        if self.sort_price_option:
            scraper_data = Sort.with_sort_price_options(self, scraper_data)
        elif self.sort_rating_option:
            scraper_data = Sort.with_sort_rating_options(self, scraper_data)

        return scraper_data


class Filter(OptionHandler):

    def with_currency(self, api):
        for data in api['data']:
            if self.currency == 'USD':
                if data['price_curr'] == 'AZN':
                    data['price_val'] = round(data['price_val'] * AZN_TO_USD, 2)
                elif data['price_curr'] == 'RUB':
                    data['price_val'] = round(data['price_val'] * RUB_TO_USD, 2)
                data['price_curr'] = 'USD'
            elif self.currency == 'AZN':
                if data['price_curr'] == 'USD':
                    data['price_val'] = round(data['price_val'] * USD_TO_AZN, 2)
                elif data['price_curr'] == 'RUB':
                    data['price_val'] = round(data['price_val'] * RUB_TO_AZN, 2)
                data['price_curr'] = 'AZN'
            elif self.currency == 'RUB':
                if data['price_curr'] == 'USD':
                    data['price_val'] = round(data['price_val'] * USD_TO_RUB, 2)
                elif data['price_curr'] == 'AZN':
                    data['price_val'] = round(data['price_val'] * AZN_TO_RUB, 2)
                data['price_curr'] = 'RUB'

        return api

    def with_price_limits(self, api):
        api['data'] = filter(lambda x: self.max_price > x['price_val'] >= self.min_price, api['data'])
        return api


class Sort(OptionHandler):

    def with_sort_price_options(self, api):
        api['data'] = sorted(api['data'], key=lambda x: x['price_val'], reverse=(self.sort_price_option == 'descending'))
        return api

    def with_sort_rating_options(self, api):
        api['data'] = sorted(api['data'], key=lambda x: x['rating_val'], reverse=(self.sort_rating_option == 'descending'))
        return api
