from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import allure

from ui.locators import base_locators
from ui.consts import CLICK_ATTEMPTS, TIMEOUT
from utils.logger import Logger

class BasePage:
    locators = base_locators.BasePageLocators
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = Logger()
        
    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)
    
    @allure.step('Поиск {locator}')
    def find(self, locator, timeout=None):
        return self.wait(timeout).until(ec.presence_of_element_located(locator))
    
    @allure.step('Ожидание, пока {locator} станет кликабельным')
    def find_waiting_clickable(self, locator, timeout=None):
        return self.wait(timeout).until(ec.element_to_be_clickable(locator))
    
    @allure.step('Проверка на доступность {locator}')
    def is_element_available(self, locator, timeout=TIMEOUT):
        try:
            self.find(locator, timeout)
        except TimeoutException:
            return False
        return True
    
    @allure.step('Подставление значения {value} в {locator}')
    def format_locator(self, locator, value=None):
        return (locator[0], locator[1].format(value))
    
    @allure.step('Заполнить поле {locator} значением {query}')
    def fill_up(self, locator, query, timeout=None):
        self.find(locator, timeout).click()
        self.find(locator).clear()
        self.find(locator).send_keys(query)
    
    @allure.step('Пролистать к {element}')
    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)
    
    @allure.step('Клик по {locator}')
    def click(self, locator, timeout=TIMEOUT):
        for i in range(CLICK_ATTEMPTS):
            try:
                self.find(locator, timeout)
                element = self.find_waiting_clickable(locator, timeout)
                self.scroll_to(element)
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_ATTEMPTS - 1:
                    raise
    
    @allure.step('Получение значения аттрибута {value} по {locator}')
    def get_attribute(self, locator, value="value", timeout=None):
        element = self.find(locator, timeout)
        value = element.get_attribute(value)
        return value
