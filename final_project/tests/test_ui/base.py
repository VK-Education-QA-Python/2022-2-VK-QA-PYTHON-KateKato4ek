import pytest 
import os
import allure

from _pytest.fixtures import FixtureRequest
from ui.pages.register_page import RegisterPage
from ui.pages.login_page import LoginPage
from ui.pages.home_page import HomePage
from fixtures import driver
from conftest import config, logger, temp_dir

class BaseCase:
    authorize = True
    
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config, logger, temp_dir, driver, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.path = temp_dir
        self.login_page = LoginPage(self.driver)
        self.register_page = RegisterPage(self.driver)
        
        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.refresh()
        self.home_page = HomePage(self.driver)
            
    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, 'browser.log')
            with open(browser_logs, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            screenshot_path = os.path.join(temp_dir, 'failed.png')
            self.driver.save_screenshot(filename=screenshot_path)
            allure.attach.file(screenshot_path, 'failed.png', allure.attachment_type.PNG)
            with open(browser_logs, 'r') as f:
                allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)
