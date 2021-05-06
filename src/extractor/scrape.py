import abc


class AbstractScraper(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _get_data(self, *args, **kwargs):
        """
        method returns either a page source or json file full of information about the searched item
        :param *args: page_count
        """
        pass

    @abc.abstractmethod
    def _extract_data(self, page_data):
        """
        this method generates an api from searched item. No filtering is applied here
        :param page_data: page source(str) or json file
        :return: dict
        """
        pass

    @abc.abstractmethod
    def _get_api(self):
        """
        with this method you get the api
        :return: dict
        """
        pass

    @abc.abstractmethod
    def __call__(self, **kwargs):
        """
        Will return scraped data in api form when called
        :param kwargs: search item and etc.
        :return: dict(api)
        """
        pass

    @staticmethod
    def _construct_api(**kwargs):
        """
        this method constructs one standard api structure with python dictionary for all child scraper classes.
        :param kwargs: api data value parameters
        :return: dict
        """
        return {
            'title': kwargs['title'],
            'price_val': kwargs['price_value'],
            'price_curr': kwargs['price_curr'],
            'url': kwargs['base_url'],
            'rating_val': kwargs['rating_val'],
            'rating_over': kwargs['rating_over'],
            'rating': kwargs['rating'],
            'shipping': kwargs['shipping'],
            'short_url': kwargs['short_url']
        }

    @staticmethod
    def _update_details(api, time_start, time_end):
        """
        this method is used to update the api dict with details of:
        execution_time: time passed when getting data from website and constructing api
        total_num: total number of found products
        :param api: api data value parameters
        :param time_start: float
        :param time_end: float
        :return: dict
        """
        api.update({
            'details': {
                'exec_time': round((time_end - time_start), 2),
                'total_num': len(api['data'])
            }
        })
        return api

    @staticmethod
    def _price_formatter(price_value):
        """
        this method cleans the price_value and returns pure float number
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
    def _printer(api):
        """
        this method prints 3 core parameters of scraped data. Use this method when debugging
        :param api: dict
        """
        for i in api['data']:
            print(f'Title: {i["title"]}')
            print(f'Price: {i["price_val"]}')
            print(f'Rating: {i["rating"]}')
            print('\n\n')
