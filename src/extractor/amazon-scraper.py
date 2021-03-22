from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

url = 'https://www.tap.az'

item_form = '//*[@id="keywords"]'
tap_button = '//*[@id="header"]/div[2]/div[1]/form/div[3]/button'
result = '*[@id="content"]/div[2]/div/div[2]/div[2]/div/div[1]/a'

driver.get(url)
driver.find_element_by_xpath(item_form).send_keys('iphone 11')
driver.find_element_by_xpath(tap_button).click()
driver.find_element_by_xpath(result)
#
# xpathes = [
#     '*[@id="content"]/div[2]/div/div[2]/div[2]/div/div[1]/a',
#     '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div[2]/a',
#     '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div[3]/a',
#     '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div[4]/a',
#     '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div[5]/a',
#     '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div[6]/a',
#     '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div[7]/a',
#     '//*[@id="content"]/div[2]/div/div[3]/div[3]/div[1]/a',
#     '//*[@id="content"]/div[2]/div/div[3]/div[3]/div[2]/a',
#     '//*[@id="content"]/div[2]/div/div[3]/div[3]/div[197]/a'
# ]
#
# urls = [driver.find_element_by_xpath(xpath) for xpath in xpathes]
# for url in urls:
#     print(url)