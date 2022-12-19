from selenium.common.exceptions import TimeoutException
import allure

from ui.pages.base_page import BasePage
from ui.locators import base_locators
from ui.consts import TIMEOUT

class LoginPage(BasePage):
    locators = base_locators.LoginPageLocators
    
    @allure.step('Авторизация')
    def login(self, username, password):
        self.fill_up(self.locators.USERNAME_FIELD, username)
        self.fill_up(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_BUTTON)
    
    @allure.step('Проверка поля юзернейм на валидацию длины')
    def check_username_input_validation(self, min_length, max_length):
        found_min_length = int(self.get_attribute(self.locators.USERNAME_FIELD, value='minlength'))
        found_max_length = int(self.get_attribute(self.locators.USERNAME_FIELD, value='maxlength'))
        
        return min_length == found_min_length and max_length == found_max_length
    
    @allure.step('Проверка валидации полей юзернейм и пароль на пустоту')
    def check_validation(self, id):
        try:
            locator = self.format_locator(self.locators.FIELD_TEMPLATE_REQUIRED, id)
            self.find(locator=locator, timeout=TIMEOUT)
        except TimeoutException:
            raise Exception('Валидация поля отсутствует')
    
    @allure.step('Проверка перехода на страницу регистрации')
    def go_to_registration_page(self):
        self.click(self.locators.CREATE_ACCOUNT_LINK)
