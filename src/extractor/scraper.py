
AZN_TO_USD = 0.59
RUB_TO_USD = 0.013
USD_TO_AZN = 1.70
RUB_TO_AZN = 0.022
USD_TO_RUB = 76.08
AZN_TO_RUB = 44.75


class Scraper:
    def __init__(self, currency, min_price, max_price, sort_option):
        self.PRICE_MAX = 10000000000
        self.currency = None if currency == 'default' is None else currency
        self.min_price = 0 if min_price is None else min_price
        self.max_price = self.PRICE_MAX if max_price is None else max_price
        self.sort_option = None if sort_option == 'default' else sort_option

    @staticmethod
    def price_formatter(price_value):
        if ' ' in price_value:
            price_value = str(price_value).replace(' ', '')
        if ',' in price_value:
            price_value = price_value.replace(',', '')
        if '$' in price_value:
            price_value = price_value.replace('$', '')
        return float(price_value)

    def with_currency(self, api):
        for data in api['data']:
            if self.currency == 'usd':
                if data['price_curr'] == 'AZN':
                    data['price_val'] = round(data['price_val'] * AZN_TO_USD, 2)
                elif data['price_curr'] == 'RUB':
                    data['price_val'] = round(data['price_val'] * RUB_TO_USD, 2)
                data['price_curr'] = 'USD'
            elif self.currency == 'azn':
                if data['price_curr'] == 'USD':
                    data['price_val'] = round(data['price_val'] * USD_TO_AZN, 2)
                elif data['price_curr'] == 'RUB':
                    data['price_val'] = round(data['price_val'] * RUB_TO_AZN, 2)
                data['price_curr'] = 'AZN'
            elif self.currency == 'rub':
                if data['price_curr'] == 'USD':
                    data['price_val'] = round(data['price_val'] * USD_TO_RUB, 2)
                elif data['price_curr'] == 'AZN':
                    data['price_val'] = round(data['price_val'] * AZN_TO_RUB, 2)
                data['price_curr'] = 'RUB'

        return api

    def with_price_limits(self, api):
        api['data'] = filter(lambda x: self.max_price > x['price_val'] >= self.min_price, api['data'])
        # api['data'] = [x for x in api['data'] if self.max_price > x['price_val'] > self.min_price]
        return api

    def with_sort_options(self, api):
        api['data'] = sorted(api['data'], key=lambda x: x['price_val'], reverse=(self.sort_option == 'descending'))
        return api

    def with_options(self, api):
        if self.currency:
            api = self.with_currency(api)
        if self.min_price != 0 or self.max_price != self.PRICE_MAX:
            api = self.with_price_limits(api)
        if self.sort_option:
            api = self.with_sort_options(api)

        return api

    @staticmethod
    def printer(api):
        for i in api['data']:
            print(f'Title: {i["title"]}')
            print(f'Price: {i["price_val"]}')
            print(f'Rating: {i["rating"]}')
            print('\n\n')
