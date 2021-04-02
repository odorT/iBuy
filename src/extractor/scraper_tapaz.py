from src.extractor.driver import chrome_driver
import time
from bs4 import BeautifulSoup


class Scrape:
    def __init__(self, item, timeout=0.4):
        self.timeout = timeout
        self.driver = chrome_driver
        self.url = 'https://tap.az/elanlar?&keywords=' + item.replace(' ', '+')
        self.clean_url = 'https://tap.az/'
        self.product_api = []
        self.item = item

    def source_page_generator(self):
        self.driver.get_driver().get(self.url)

        number_of_scrolls = 0
        reached_page_end = False
        last_height = self.driver.get_driver().execute_script("return document.body.scrollHeight")
        while not reached_page_end:
            self.driver.get_driver().execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.timeout)
            new_height = self.driver.get_driver().execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                reached_page_end = True
            else:
                last_height = new_height
            number_of_scrolls += 1

        return self.driver.get_driver().page_source

    def api_generator(self):
        final_page = self.source_page_generator()
        start_string = '<div class="js-endless-container products endless-products">'
        end_string = '<div class="pagination_loading">'
        main_html = str(final_page)[str(final_page).find(start_string):]
        main_html = main_html[:main_html.find(end_string)]

        soup = BeautifulSoup(main_html, 'lxml')
        product_list = soup.select("div[class^=products-i]")

        for item in product_list:
            for link in item.find_all('a', target='_blank', href=True):
                try:
                    base_url = self.clean_url + link['href']
                    title = link.find('div', class_='products-name').text
                    price = link.find('span', class_='price-val').text + link.find('span', class_='price-cur').text
                except:
                    base_url = None
                    title = None
                    price = None

                self.product_api.append({
                    'data': {
                        'title': title,
                        'price': price,
                        'url': base_url,
                        'rating': None,
                        'short_url': 'www.tap.az'
                    },
                    'total_num': '',
                    'exec_time': ''
                })

        return self.product_api

    def driver_close(self):
        self.driver.get_driver().close()
        self.driver.get_driver().quit()

    def printer(self):
        for num, i in enumerate(self.product_api):
            print(num, f"Title: {i['data']['title']}, Price: {i['data']['price']}")

    def run(self):
        self.source_page_generator()
        self.api_generator()
        self.printer()
