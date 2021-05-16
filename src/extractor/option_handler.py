from __future__ import annotations
from abc import ABC, abstractmethod
import json
import os

with open(os.path.abspath("src/currencies.json")) as file:
    currencies = json.load(file)
print(os.path.abspath("src/currencies.json"))


class OptionsHandler:
    def __init__(self, filter_handler: OptionHandlerInterface, sort_handler: OptionHandlerInterface):
        self.filter_handler = filter_handler
        self.sort_handler = sort_handler

    def operation(self, api):
        api = self.sort_handler.handle(api)
        api = self.filter_handler.handle(api)
        return api


class OptionHandlerInterface(ABC):

    @abstractmethod
    def define_options(self, **kwargs):
        """
        method defines provided options
        :param kwargs: dict of options
        """
        pass

    @abstractmethod
    def handle(self, api):
        """
        this method will  handle given api and return the new one
        :param api: dict
        :return: dict
        """
        pass


class Filter(OptionHandlerInterface):
    def __init__(self):
        self.PRICE_MAX = 10000000000
        self.PRICE_MIN = 0

    def define_options(self, **kwargs):
        self.currency = None if kwargs['currency'] == 'default' else kwargs['currency']
        self.min_price = self.PRICE_MIN if kwargs['min_price'] is None or kwargs['min_price'] < self.PRICE_MIN else kwargs['min_price']
        self.max_price = self.PRICE_MAX if kwargs['max_price'] is None else kwargs['max_price']

    def with_currency(self, api):
        for data in api['data']:
            if self.currency == 'USD':
                if data['price_curr'] == 'AZN':
                    data['price_val'] = round(data['price_val'] * currencies["AZN_TO_USD"], 2)
                elif data['price_curr'] == 'RUB':
                    data['price_val'] = round(data['price_val'] * currencies["RUB_TO_USD"], 2)
                data['price_curr'] = 'USD'
            elif self.currency == 'AZN':
                if data['price_curr'] == 'USD':
                    data['price_val'] = round(data['price_val'] * currencies["USD_TO_AZN"], 2)
                elif data['price_curr'] == 'RUB':
                    data['price_val'] = round(data['price_val'] * currencies["RUB_TO_AZN"], 2)
                data['price_curr'] = 'AZN'
            elif self.currency == 'RUB':
                if data['price_curr'] == 'USD':
                    data['price_val'] = round(data['price_val'] * currencies["USD_TO_RUB"], 2)
                elif data['price_curr'] == 'AZN':
                    data['price_val'] = round(data['price_val'] * currencies["AZN_TO_RUB"], 2)
                data['price_curr'] = 'RUB'

        return api

    def with_price_limits(self, api):
        # api['data'] = filter(lambda x: self.max_price > x['price_val'] >= self.min_price, api['data'])
        api['data'] = [x for x in api['data'] if self.max_price > x['price_val'] >= self.min_price]

        return api

    def handle(self, scraped_data):
        if self.currency:
            scraped_data = self.with_currency(scraped_data)
        if self.min_price != 0 or self.max_price != self.PRICE_MAX:
            scraped_data = self.with_price_limits(scraped_data)

        return scraped_data


class Sort(OptionHandlerInterface):
    def define_options(self, **kwargs):
        self.sort_price_option = None if kwargs['sort_price_option'] == 'default' else kwargs['sort_price_option']
        self.sort_rating_option = None if kwargs['sort_rating_option'] == 'default' else kwargs['sort_rating_option']

    def with_sort_price_options(self, api):
        api['data'] = sorted(api['data'], key=lambda x: x['price_val'], reverse=(self.sort_price_option == 'descending'))
        return api

    def with_sort_rating_options(self, api):
        api['data'] = sorted(api['data'], key=lambda x: x['rating_val'], reverse=(self.sort_rating_option == 'descending'))
        return api

    def handle(self, scraped_data):
        if self.sort_price_option:
            scraped_data = self.with_sort_price_options(scraped_data)
        elif self.sort_rating_option:
            scraped_data = self.with_sort_rating_options(scraped_data)

        return scraped_data
