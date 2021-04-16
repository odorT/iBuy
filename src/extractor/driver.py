from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


class Driver:
    def __init__(self, headless):
        self.headless = headless
        self.options = ChromeOptions()
        self.options.add_argument("--window-size=1600, 490")
        self.options.add_argument("--disable-infobars")
        self.options.headless = self.headless
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        self.driver.implicitly_wait(30)

    def get_driver(self):
        return self.driver

    def stop_driver(self):
        print('>> Quiting and closing the browser')
        self.driver.close()
        self.driver.quit()


tapaz_driver = Driver(True)
amazon_driver = Driver(True)
# aliexpress_driver = Driver(False)
