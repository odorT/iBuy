from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


# from selenium.webdriver.common.proxy import Proxy, ProxyType


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Driver(metaclass=Singleton):
    def __init__(self, headless):
        self.headless = headless
        self.options = ChromeOptions()
        self.options.add_argument("--window-size=1600, 490")
        self.options.add_argument("--disable-infobars")
        self.options.headless = self.headless
        self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=self.options)
        self.driver.implicitly_wait(30)

        # self.proxy = Proxy()
        # self.proxy.proxy_type = ProxyType.MANUAL
        # self.proxy.http_proxy = "143.198.72.156:3128"
        # # self.proxy.socks_proxy = "143.198.72.156:3128"
        # # self.proxy.ssl_proxy = "143.198.72.156:3128"
        #
        # self.capabilities = webdriver.DesiredCapabilities.CHROME
        # self.proxy.add_to_capabilities(self.capabilities)

    def get_driver(self):
        return self.driver

    # def get_driver_with_proxy(self):
    #     self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options,
    #                                    desired_capabilities=self.capabilities)
    #     return self.get_driver()

    def stop_driver(self):
        print('>> Quiting and closing the browser')
        self.driver.close()
        self.driver.quit()
