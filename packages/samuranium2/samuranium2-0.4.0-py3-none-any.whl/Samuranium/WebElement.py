import time
from timeit import default_timer as timer

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement

from Samuranium.Config import Config
from Samuranium.utils.classes import get_class_variables_dict
from Samuranium.utils.time import get_current_time


class WebElement:
    """
    Web element class
    """

    def __init__(self, samuranium_instance, selector, exact_selector=False, max_wait_time=None):
        self.config = Config()
        self.browser = samuranium_instance.driver
        self.logger = samuranium_instance.logger
        self.selector = selector
        self.exact_selector = exact_selector
        self.max_wait_time = max_wait_time if max_wait_time else self.config.default_wait_time
        self.__element = None

    @property
    def element(self):
        """
        :return: web element
        """
        if not self.__element:
            self.__element: SeleniumWebElement = self.__find_element()
        return self.__element

    def update(self):
        self.__element = None
        return self.element

    @property
    def text(self):
        return self.element.text

    def is_present(self):
        return self.element is not None

    def ensure_element_exists(self):
        if not self.is_present():
            raise NoSuchElementException(
                'Element with selector "{}" was not found after {} seconds'.
                format(self.selector, self.max_wait_time))

    @staticmethod
    def __finder_strategies():
        return get_class_variables_dict(By)

    @staticmethod
    def __xpath_strategies():
        return {'match_xpath': '{}', 'exact_text': '//*[text()="{}"]',
                'normalize_text': '//*[not(self::script)][text()[normalize-space()="{}"]]',
                'contains_text': '//*[not(self::script)][contains(text(),"{}")]',
                'normalize_contains_text':
                    '//*[not(self::script)][contains(normalize-space(.), "{}")]',
                }

    @staticmethod
    def __css_strategies():
        return {'match_css': '{}', 'class_name': '.{}', 'id': '#{}'}

    def __find_element(self):
        start_time = get_current_time()
        while timer() - start_time < self.max_wait_time:
            for strategy_name, method in self.__finder_strategies().items():
                try:
                    if method == By.XPATH:
                        element: SeleniumWebElement = self.__find_by_xpath()
                        if element:
                            return element
                    elif method == By.CSS_SELECTOR:
                        element: SeleniumWebElement = self.__find_by_css_selector()
                        if element:
                            return element
                    else:
                        element: SeleniumWebElement = self.__find_by_strategy(method)
                        if element:
                            return element
                    if not self.exact_selector:
                        element: SeleniumWebElement = self.browser.find_element(method,
                                                                                self.selector)
                        return element
                except NoSuchElementException:
                    pass
        self.logger.error(f'Element with selector: {self.selector} was not found after '
                          f'{self.max_wait_time}')
        return None

    def __find_by_xpath(self):
        for finder_name, xpath_strategy in self.__xpath_strategies().items():
            try:
                if self.exact_selector:
                    return self.browser.find_element_by_xpath(self.selector)
                return self.browser.find_element_by_xpath(xpath_strategy.format(self.selector))
            except NoSuchElementException:
                pass
        return None

    def __find_by_css_selector(self):
        for finder_name, css_strategy in self.__css_strategies().items():
            try:
                if self.exact_selector:
                    return self.browser.find_element_by_css_selector(self.selector)
                return self.browser.find_element_by_css_selector(css_strategy.format(self.selector))
            except NoSuchElementException:
                pass
        return None

    def __find_by_strategy(self, strategy):
        try:
            return self.browser.find_element(strategy, self.selector)
        except NoSuchElementException:
            pass
        return None

    def is_displayed(self):
        return self.element.is_displayed()

    def exists(self):
        return self.__element and self.is_present()

    def click(self):
        try:
            self.element.click()
            return True
        except Exception as e:
            self.logger.error('Not possible to click on element with selector {}'.format(
                self.selector), e)
            return False

    def input_text(self, text):
        for _ in range(5):
            try:
                self.element.send_keys(text)
                return True
            except Exception as e:
                self.logger.error('Not possible to send text {} to element with selector {}'.format(
                    text, self.selector), e)
                self.logger.debug("Waiting 1 second until element is interactable")
                time.sleep(1)
        return False
