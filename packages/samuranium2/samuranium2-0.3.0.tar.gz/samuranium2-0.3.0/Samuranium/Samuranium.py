from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from Samuranium.Logger import Logger
from Samuranium.WebElement import WebElement


class Samuranium:
    def __init__(self, custom_logger=None, headless=False):
        self.headless = headless
        self.max_wait_time = 5
        self.logger = custom_logger or Logger()
        self.driver = self.get_driver()

    def get_driver(self):
        if self.headless:
            self.logger.debug('Starting chrome in headless mode')
            options = ChromeOptions()
            options.add_argument('-headless')
            options.add_argument("-disable-gpu")
            options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            return webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                    chrome_options=options)
        self.logger.debug('Starting chrome')
        return webdriver.Chrome(ChromeDriverManager().install())

    def navigate(self, url):
        self.driver.get(url)

    def find_element(self, selector: str = None,
                     max_wait_time: float = None) -> WebElement:
        return WebElement(self, selector=selector, max_wait_time=max_wait_time)

