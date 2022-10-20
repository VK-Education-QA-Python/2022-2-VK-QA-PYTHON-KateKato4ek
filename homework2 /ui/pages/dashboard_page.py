from ui.pages.base_page import BasePage
from ui.locators import base_locators
from ui.pages.campaign_page import CampaignPage
from ui.pages.audience_page import AudiencePage

class DashboardPage(BasePage):
    locators = base_locators.DashboardPageLocators
    
    def get_campaign_page(self):
        self.click(self.locators.CAMPAIGNS_BTN_LOCATOR)
        
        return CampaignPage(driver=self.driver)
    
    def get_audience_page(self):
        self.go_to_audience_page()
        
        return AudiencePage(driver=self.driver)
    
    def go_to_audience_page(self):
        self.click(self.locators.AUDIENCE_BTN_LOCATOR)
