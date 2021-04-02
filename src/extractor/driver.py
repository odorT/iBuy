from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class Driver(metaclass=Singleton):
    __metaclass__ = Singleton

    def __init__(self, headless):
        self.headless = headless
        self.options = ChromeOptions()
        self.options.add_argument("--window-size=1600, 490")
        self.options.headless = self.headless
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        self.driver.implicitly_wait(30)

    def get_driver(self):
        return self.driver

    def set_headless(self, headless):
        self.headless = headless

    def stop_chrome(self):
        print('>> Quiting and closing the browser')
        self.driver.close()
        self.driver.quit()


chrome_driver = Driver(False)
