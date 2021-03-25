from helium import *
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

options = ChromeOptions()
options.add_argument('--start-maximized')
options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = 'https://tap.az/'

set_driver(driver)
go_to(url)
write('Iphone 12', into='Məsələn, iPhone X')
click('TAP')

found_products = find_all(S('.categories-products-found'))
total_product_num = int(str(found_products).split('">')[1].split(' elan')[0])
item_urls = []
container = find_all(S('.products-i rounded bumped featured vipped '))

print(container)
# for _ in range(total_product_num):


# items_list.extend(find_all(S('.products-name')))
# driver.quit()
# kill_browser()