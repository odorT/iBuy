from src.extractor.driver import tapaz_driver
from src.extractor.scrape import Scraper
import time
from bs4 import BeautifulSoup


class Scrape_tapaz(Scraper):
    def __init__(self, **kwargs):
        self.item = kwargs['item']
        self.timeout = kwargs['timeout']
        self.mode = kwargs['mode']
        self.driver = tapaz_driver.get_driver()
        self.url = 'https://tap.az/elanlar?&keywords=' + self.item.replace(' ', '+')
        self.product_api = {}

    def get_data(self):
        global time_start
        time_start = time.time()

        self.driver.get(self.url)

        if self.mode == 'fast':
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.timeout)
        elif self.mode == 'slow':
            number_of_scrolls = 0
            reached_page_end = False
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while not reached_page_end:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.timeout)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if last_height == new_height:
                    reached_page_end = True
                else:
                    last_height = new_height
                number_of_scrolls += 1

        return self.driver.page_source

    def api_generator(self, page_data):
        final_page = page_data
        start_string = '<div class="js-endless-container products endless-products">'
        end_string = '<div class="pagination_loading">'
        main_html = str(final_page)[str(final_page).find(start_string):]
        main_html = main_html[:main_html.find(end_string)]

        soup = BeautifulSoup(main_html, 'lxml')
        product_list = soup.select("div[class^=products-i]")
        api = {'data': []}

        for item in product_list:
            for link in item.find_all('a', target='_blank', href=True):
                try:
                    base_url = 'https://tap.az/' + link['href']
                    title = link.find('div', class_='products-name').text
                    price_value = self.price_formatter(link.find('span', class_='price-val').text)
                    price_curr = link.find('span', class_='price-cur').text

                    api['data'].append({
                        'title': title,
                        'price_val': price_value,
                        'price_curr': price_curr,
                        'url': base_url,
                        'rating_val': 0,
                        'rating_over': None,
                        'rating': None,
                        'shipping': None,
                        'short_url': 'www.tap.az'
                    })
                except:
                    continue

        time_end = time.time()

        api.update({
            'details': {
                'exec_time': round((time_end - time_start), 2),
                'total_num': len(api['data'])
            }
        })

        return api

    def get_api(self):
        page_data = self.get_data()
        self.product_api = self.api_generator(page_data=page_data)

        return self.product_api
