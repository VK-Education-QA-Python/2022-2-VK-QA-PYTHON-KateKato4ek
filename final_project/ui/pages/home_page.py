import allure

from ui.pages.base_page import BasePage
from ui.locators import base_locators

class HomePage(BasePage):
    locators = base_locators.HomePageLocators

    @allure.step('Разлогирование')
    def log_out(self):
        self.click(self.locators.LOG_OUT_BTN)
    
    @allure.step('Переход на домашнюю страницу')
    def go_to_home_page(self):
        self.click(self.locators.HOME_BTN)
    
    @allure.step('Проверка редиректа на новую страницу')
    def check_redirect(self, title, expected):
        found_locator = self.format_locator(self.locators.CENTRAL_CIRCLE_BTN, title)
        self.click(found_locator)
        
        if len(self.driver.window_handles) != 2:
            return False
        
        self.driver.switch_to.window(self.driver.window_handles[1])
        
        return expected in self.driver.page_source
    
    @allure.step('Проверка присутствия факта о Python')
    def check_fact_about_python_precence(self):
        element = self.find(self.locators.PYTHON_FACT)
        fact = element.text
        
        return fact != None and fact != ''

    @allure.step('Проверка на наличие VK id')
    def check_has_vk_id(self, vk_id):
        element = self.find(self.locators.VK_ID)
        founded_vk_id = element.text
        
        return str(vk_id) in founded_vk_id
    
    @allure.step('Проверка на отсутсвие VK id')
    def check_no_vk_id(self):
        return self.is_element_available(self.locators.VK_ID) == False
