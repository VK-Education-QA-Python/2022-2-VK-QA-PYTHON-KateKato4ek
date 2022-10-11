import pytest

import ui.locators.base_locators as bsl
from base import BaseCase
from consts import INCORRECT_EMAIL, INCORRECT_PASSWORD

class TestOne(BaseCase):
    def test_login(self):
        assert "Target" in self.driver.title
        
        self.login()
        account_found = self.check_element_presence(bsl.ACCOUNT_BUTTON_LOCATOR)
        
        assert account_found
    
    def test_login_wrong_email(self):
        assert "Target" in self.driver.title
        
        self.login(email = INCORRECT_EMAIL)
        account_found = self.check_element_presence(bsl.ACCOUNT_BUTTON_LOCATOR)
        
        assert account_found == False
    
    def test_login_wrong_password(self):
        assert "Target" in self.driver.title
        
        self.login(password = INCORRECT_PASSWORD)
        account_found = self.check_element_presence(bsl.ACCOUNT_BUTTON_LOCATOR)
        
        assert account_found == False
    
    def test_logout(self):
        assert "Target" in self.driver.title
        
        self.login()
        self.click_logout_button()
        is_logged_out = self.check_element_presence(bsl.LOGIN_BUTTON_LOCATOR)
        
        assert is_logged_out
        
    def test_contact_information(self):
        NAME = "username"
    
        assert "Target" in self.driver.title
        
        self.login()
        self.fulfilling_contact_information(NAME)
        is_conctact_information_correct = self.check_contact_information(NAME)
        
        assert is_conctact_information_correct
    
    @pytest.mark.parametrize(
        'tab_locator, element_locator',
        [
            pytest.param(
                bsl.PROFILE_BUTTON_LOCATOR,
                bsl.NAME_FIELD_LOCATOR
            ),
            pytest.param(
                bsl.TOOLS_BUTTON_LOCATOR,
                bsl.LIST_OF_FIDS_LOCATOR
            )
        ]
    )
    def test_go_to_profile(self, tab_locator, element_locator):
        assert "Target" in self.driver.title
        
        self.login()
        self.go_to_tab_page(tab_locator)
        
        element_found = self.check_element_presence(element_locator)
        assert element_found
