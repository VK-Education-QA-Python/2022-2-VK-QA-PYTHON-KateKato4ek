import pytest 
import time

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException

import ui.locators.base_locators as bsl

from consts import (
    TIMEOUT,
    CORRECT_EMAIL,
    CORRECT_PASSWORD,
    ATTEMPS_COUNT,
)

class BaseCase:
    driver = None
    
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver
        
    def find_waiting_presence(self, locator, timeout = TIMEOUT):
        element_presence = ec.presence_of_element_located(locator)
        element = wait(self.driver, timeout).until(element_presence)
        return element
    
    def find_waiting_clickable(self, locator, timeout = TIMEOUT):
        element_presence = ec.element_to_be_clickable(locator)
        element = wait(self.driver, timeout).until(element_presence)
        return element
    
    def find(self, locator):
        element = self.driver.find_element(*locator)
        return element
    
    def check_element_presence(self, locator, timeout = TIMEOUT):
        element_presence = ec.presence_of_element_located(locator)
        try:
            wait(self.driver, timeout).until(element_presence)
            element_found = True
        except TimeoutException:
            element_found = False
        return element_found
    
    def login(self, email = CORRECT_EMAIL, password = CORRECT_PASSWORD):
        login_button = self.find_waiting_presence(bsl.LOGIN_BUTTON_LOCATOR)
        login_button.click()
        
        email_input = self.find(bsl.EMAIL_INPUT_LOCATOR)
        email_input.clear()
        email_input.send_keys(email)
        
        password_input = self.find(bsl.PASWORD_INPUT_LOCATOR)
        password_input.clear()
        password_input.send_keys(password)
        
        send_button = self.find(bsl.SEND_BUTTON_LOCATOR)
        send_button.click()
    
    def click_logout_button(self):
        for i in range(ATTEMPS_COUNT):
            try:
                account_button = self.find_waiting_presence(bsl.ACCOUNT_BUTTON_LOCATOR)
                account_button.click()
                
                logout_button = self.find_waiting_clickable(bsl.LOGOUT_BUUTTON_LOCATOR)
                time.sleep(1)
                logout_button.click()
                
                break
            except:
                if i + 1 == ATTEMPS_COUNT:
                    raise
                time.sleep(0.5)
    
    def fulfilling_contact_information(self, name):
        self.go_to_tab_page(bsl.PROFILE_BUTTON_LOCATOR)
        
        name_field = self.find_waiting_presence(bsl.NAME_FIELD_LOCATOR)
        name_field.clear()
        name_field.send_keys(name)
        
        save_button = self.find(bsl.SAVE_BUTTON_LOCATOR)
        save_button.click()

    def check_contact_information(self, name):
        self.driver.refresh()
        
        name_field = self.find_waiting_presence(bsl.NAME_FIELD_LOCATOR)
        name_input_value = name_field.get_attribute("value")
        return name_input_value == name

    def go_to_tab_page(self, locator):
        tab_button = self.find_waiting_presence(locator)
        tab_button.click()
