import pytest 

from _pytest.fixtures import FixtureRequest
from ui.pages.dashboard_page import DashboardPage
from ui.fixtures import driver
from conftest import config, logger, temp_dir

class BaseCase:
    authorize = True
    
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config, logger, temp_dir, driver, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.path = temp_dir
        
        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.refresh()
            self.dashboard_page = DashboardPage(driver)
