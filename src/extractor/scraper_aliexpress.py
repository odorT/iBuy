from src.extractor.driver import aliexpress_driver
import time
from bs4 import BeautifulSoup


class Scrape:
    def __init__(self, item):
        self.driver = aliexpress_driver.get_driver()
        self.url = 'https://www.aliexpress.com/wholesale?catId=0&SearchText=' + item.replace(' ', '+')
        self.clean_url = 'https://www.aliexpress.com/'
        self.product_api = {'data': []}
        self.item = item

    def source_page_generator(self):
        self.driver.get(self.url)
        try:
            # for i in range(10):
            popup_close_button = self.driver.find_element_by_xpath(f'./html/body/div[7]/div[2]/div/a')
            popup_close_button.click()
        except:
            pass

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self.driver.page_source

    def api_generator(self):
        time_start = time.time()  # to calculate overall execution time

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

                self.product_api['data'].append({
                    'title': title,
                    'price': price,
                    'url': base_url,
                    'rating': None,
                    'short_url': 'www.tap.az'
                })

        time_end = time.time()

        self.product_api.update({
            'details': {
                'exec_time': round((time_end - time_start), 2),
                'total_num': len(self.product_api['data'])
            }
        })

        return self.product_api

    def driver_close(self):
        self.driver.close()
        self.driver.quit()

    def printer(self):
        for i in self.product_api['data']:
            print(f'Title : {i["title"]}, price : {i["price"]}')
        print(self.product_api['details']['exec_time'])

    def run(self):
        self.source_page_generator()
        # self.printer()
