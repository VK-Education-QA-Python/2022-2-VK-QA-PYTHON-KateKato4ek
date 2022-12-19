from selenium.common.exceptions import TimeoutException
import allure

from ui.pages.base_page import BasePage
from ui.locators import base_locators
from ui.consts import TIMEOUT

class RegisterPage(BasePage):
    locators = base_locators.RegisterPageLocators
    
    @allure.step('Регистрация с данными {name}, {surname}, {middlename}, {username}, {email}, {password}, {confirmpassword}')
    def register(self, name, surname, middlename, username, email, password, confirmpassword):
        self.fill_up(self.locators.NAME_FIELD, name)
        self.fill_up(self.locators.SURNAME_FIELD, surname)
        self.fill_up(self.locators.MIDDLENAME_FIELD, middlename)
        self.fill_up(self.locators.USERNAME_FIELD, username)
        self.fill_up(self.locators.EMAIL_FIELD, email)
        self.fill_up(self.locators.PASSWORD_FIELD, password)
        self.fill_up(self.locators.CONFIRMPASSWORD_FIELD, confirmpassword)
        self.click(self.locators.CHECKBOX)
        self.click(self.locators.REGISTER_BUTTON)
    
    @allure.step('Переход на страницу регистрации')
    def go_to_login_page(self):
        self.click(self.locators.LOGIN_IN_LINK)
        
    @allure.step('Проверка валидации полей')
    def check_validation(self, id):
        try:
            locator = self.format_locator(self.locators.FIELD_TEMPLATE_REQUIRED, id)
            self.find(locator=locator, timeout=TIMEOUT)
        except TimeoutException:
            raise Exception('Валидация поля отсутствует')
    
    @allure.step('Проверка минимальной и максимальной длины значений для поля id={id}')
    def check_field_length(self, id, min_length, max_length):
        locator = self.format_locator(self.locators.FIELD_TEMPLATE, id)
        found_min_length = self.get_attribute(locator, value='minlength')
        found_max_length = self.get_attribute(locator, value='maxlength')
        
        if min_length != 0:
            valid = found_min_length is not None and min_length <= int(found_min_length)
        else:
            valid = found_min_length is None or min_length == int(found_min_length)
        
        valid = valid and found_max_length is not None and max_length >= int(found_max_length)
        
        return valid
