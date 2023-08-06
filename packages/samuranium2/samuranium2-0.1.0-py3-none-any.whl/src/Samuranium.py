from timeit import default_timer as timer
from typing import Optional, Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from webdriver_manager.chrome import ChromeDriverManager

from src.Logger import Logger
from src.WebElement import WebElement


class Samuranium:
    def __init__(self, custom_logger=None):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.max_wait_time = 2
        self.logger = Logger()

    def navigate(self, url):
        self.driver.get(url)

    def find_element(self, selector: str = None, strategy: By = None,
                     max_wait_time: float = None, wait=True) -> WebElement:
        return WebElement(self, selector)

