from ui.pages.base_page import BasePage
from ui.locators import base_locators
from ui.utils.utils import random_string
from consts import DAYMONEYAMOUNT, TOTALMONEYAMOUNT, TIMEOUT


class CampaignPage(BasePage):
    locators = base_locators.CampaignPageLocators
    
    def __init__(self, driver):
        self.campaign_name = None
        super(CampaignPage, self).__init__(driver)
    
    def create_new_campaign(self, image_path):
        self.campaign_name = random_string()
    
        if self.is_element_available(self.locators.CREATE_NEW_CAMPAIGN_BTN_LOCATOR):
            self.click(self.locators.CREATE_NEW_CAMPAIGN_BTN_LOCATOR)
        else:
            self.click(self.locators.CREATE_NEW_CAMPAIGN_ONBOARDING_BTN_LOCATOR)
            
        self.click(self.locators.TRAFFIC_BTN_LOCATOR, timeout=TIMEOUT)
        link = self.campaign_name + '.com'
        self.fill_up(self.locators.ENTER_LINK_FLD_LOCATOR, link, timeout=TIMEOUT)
        self.click(self.locators.CLEAR_NAME_FLD_BTN)
        self.fill_up(self.locators.CAMPAIGN_NAME_INPUT_FLD_LOCATOR, self.campaign_name)
        self.fill_up(self.locators.DAY_BUDGET_FLD_LOCATOR, DAYMONEYAMOUNT, timeout=TIMEOUT)
        self.fill_up(self.locators.TOTAL_BUDGET_FLD_LOCATOR, TOTALMONEYAMOUNT)
        self.click(self.locators.BANNER_BTN_LOCATOR)
        self.find(self.locators.IMAGE_INPUT_BTN_LOCATOR).send_keys(image_path)
        self.fill_up(self.locators.BANNER_NAME_INPUT, self.campaign_name)
        self.click(self.locators.SAVE_AD_BTN_LOCATOR)
        self.click(self.locators.CREATE_CAMPAIGN_BTN, timeout=TIMEOUT)
    
    def is_campaign_created(self):
        self.fill_up(self.locators.SEARCH_CANPAIGN_FLD_LOCATOR, self.campaign_name, timeout=TIMEOUT)
        
        return not self.is_element_available(self.locators.NO_CAMPAIGN_FOUND_LOCATOR)
    
    def delete_campaign_page(self):
        self.fill_up(self.locators.SEARCH_CANPAIGN_FLD_LOCATOR, self.campaign_name, timeout=TIMEOUT)
        campaign_found_locator = self.format_locator(self.locators.FOUND_CAMPAGN_LOCATOR, self.campaign_name)
        self.click(campaign_found_locator, timeout=TIMEOUT)
        self.click(self.locators.CHECK_CREATED_CAMPAIGN_LOCATOR)
        self.click(self.locators.ACTIONS_CAMPAIGN_BTN_LOCATOR)
        self.click(self.locators.DELETE_CAMPAIGN_BTN_LOCATOR, timeout=TIMEOUT)
