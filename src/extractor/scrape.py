import abc


class Scraper(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_data(self):
        """
        method returns either a page source or json file full of information about the searched item
        """
        pass

    @abc.abstractmethod
    def api_generator(self, page_data):
        """
        this method generates an api from searched item. No filtering is applied here
        :param page_data: page source(str) or json file
        :return: dict
        """
        pass

    @abc.abstractmethod
    def get_api(self):
        """
        with this method you get the api
        :return: dict
        """
        pass

    @staticmethod
    def price_formatter(price_value):
        """
        this method cleans the price_value and returns pure number
        :param price_value: string
        :return: float
        """
        if ' ' in price_value:
            price_value = str(price_value).replace(' ', '')
        if ',' in price_value:
            price_value = price_value.replace(',', '')
        if '$' in price_value:
            price_value = price_value.replace('$', '')
        return float(price_value)

    @staticmethod
    def printer(api):
        """
        this method prints 3 core parameters of scraped data. Use this method for debugging
        :param api: dict
        """
        for i in api['data']:
            print(f'Title: {i["title"]}')
            print(f'Price: {i["price_val"]}')
            print(f'Rating: {i["rating"]}')
            print('\n\n')
