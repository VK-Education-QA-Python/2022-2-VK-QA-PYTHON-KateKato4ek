from ui.pages.base_page import BasePage
from ui.locators import base_locators
from consts import TIMEOUT

class MainPage(BasePage):
    locators = base_locators.MainPageLocators
    
    def login(self, email, password):
        self.click(self.locators.LOGIN_BUTTON_LOCATOR, timeout=TIMEOUT)
        self.fill_up(self.locators.EMAIL_INPUT_LOCATOR, email, timeout=TIMEOUT)
        self.fill_up(self.locators.PASSWORD_INPUT_LOCATOR, password)
        self.click(self.locators.AUTH_BUTTON_LOCATOR)
