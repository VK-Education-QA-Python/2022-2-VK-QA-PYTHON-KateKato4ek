from ui.pages.base_page import BasePage
from ui.locators import base_locators
from ui.utils.utils import random_string
from consts import VK_EDC_LINK, TIMEOUT


class AudiencePage(BasePage):
    locators = base_locators.AudiencePageLocators
    
    def __init__(self, driver):
        self.segment_name = None
        super(AudiencePage, self).__init__(driver)
    
    def __click_on_create_button(self):
        if self.is_element_available(self.locators.CREATE_SEGMENT_BTN_LOCATOR):
            self.click(self.locators.CREATE_SEGMENT_BTN_LOCATOR)
        else:
            self.click(self.locators.CREATE_SEGMENT_ONBOARDING_BTN_LOCATOR)
    
    def __create_segment(self):
        self.click(self.locators.PUT_CHECK_BTN_LOCATOR)
        self.click(self.locators.ADD_SEGMENT_BTN_LOCATOR)
        self.segment_name = random_string()
        self.fill_up(self.locators.SEGMENT_NAME_FIELD_LOCATOR, self.segment_name)
        self.click(self.locators.APPROVE_CREATE_SEGMENT_BTN_LOCATOR)

    def create_segment(self):
        self.__click_on_create_button()
        self.__create_segment()

    def create_segment_with_link(self):
        self.__click_on_create_button()
        self.click(self.locators.GROUPS_VK_OK_IN_LIST_BTN_LOCATOR)
        self.__create_segment()
    
    def is_segment_created(self):
        self.fill_up(self.locators.FIND_CREATED_SEGMENT_FLD_LOCATOR, self.segment_name, timeout=TIMEOUT)
        
        return not self.is_element_available(self.locators.NO_SEGMENT_FOUND_LOCATOR)
    
    def delete_segment(self):
        self.fill_up(self.locators.FIND_CREATED_SEGMENT_FLD_LOCATOR, self.segment_name, timeout=TIMEOUT)
        campaign_found_locator = self.format_locator(self.locators.FOUND_SEGMENT_LOCATOR, self.segment_name)
        self.click(campaign_found_locator, timeout=TIMEOUT)
        self.click(self.locators.CHECK_CREATED_SEGMENT_LOCATOR)
        self.click(self.locators.ACTIONS_BTN_LOCATOR)
        self.click(self.locators.DELETE_AUD_SEG_BTN_LOCATOR, timeout=TIMEOUT)
    
    def add_source(self):
        self.click(self.locators.GROUPS_BTN_LOCATOR, timeout=TIMEOUT)   
        self.fill_up(self.locators.LINK_GROUPS_INPUT_FLD_LOCATOR, VK_EDC_LINK)
        self.click(self.locators.SHOW_BTN_LOCATOR, timeout=TIMEOUT)
        self.click(self.locators.VK_EDU_BTN_LOCATOR)
        self.click(self.locators.ADD_SELCTED_BTN_LOCATOR)

    def delete_source(self):
        self.click(self.locators.GROUPS_BTN_LOCATOR)
        self.click(self.locators.DELETE_SOURCE_BTN)
        self.click(self.locators.CONFIRM_DELETE_BTN_LOCATOR)
