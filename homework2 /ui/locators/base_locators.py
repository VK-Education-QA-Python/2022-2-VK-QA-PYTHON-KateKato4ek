from selenium.webdriver.common.by import By

class BasePageLocators:
    pass

class MainPageLocators(BasePageLocators):
    LOGIN_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")
    EMAIL_INPUT_LOCATOR = (By.XPATH, "//input[contains(@class, 'authForm-module-input') and @name='email']")
    PASSWORD_INPUT_LOCATOR = (By.XPATH, "//input[contains(@class, 'authForm-module-inputPassword') and @name='password']")
    AUTH_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'authForm-module-button')]")

class DashboardPageLocators(BasePageLocators):
    CAMPAIGNS_BTN_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-campaigns')]")
    AUDIENCE_BTN_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-segments')]")

class CampaignPageLocators(BasePageLocators):
    TRAFFIC_BTN_LOCATOR = (By.XPATH, "//div[contains(@class, 'traffic')]")
    CREATE_NEW_CAMPAIGN_BTN_LOCATOR = (By.XPATH, "//div[contains(@class, 'createButtonWrap')]/div")
    CREATE_NEW_CAMPAIGN_ONBOARDING_BTN_LOCATOR = (By.XPATH, "//a[contains(@href, '/campaign/new')]")
    ENTER_LINK_FLD_LOCATOR = (By.XPATH, "//input[contains(@class, 'mainUrl-module-searchInput')]")
    CAMPAIGN_NAME_INPUT_FLD_LOCATOR = (By.XPATH, "//div[contains(@class, 'input_campaign-name')]//input")
    DAY_BUDGET_FLD_LOCATOR = (By.XPATH, "//input[@data-test='budget-per_day']")
    TOTAL_BUDGET_FLD_LOCATOR = (By.XPATH, "//input[@data-test='budget-total']")
    BANNER_BTN_LOCATOR = (By.ID, "patterns_banner_4")
    IMAGE_INPUT_BTN_LOCATOR = (By.XPATH, "//div[contains(@class,'roles-module-buttonWrap')]//input")
    BANNER_NAME_INPUT = (By.XPATH, "//input[@data-name='banner-name']")
    CLEAR_NAME_FLD_BTN = (By.XPATH, "//div[contains (@class, 'input__clear')] ")
    SAVE_AD_BTN_LOCATOR = (By.XPATH, "//div[@data-test='submit_banner_button']")
    CREATE_CAMPAIGN_BTN = (By.XPATH, "//div[contains(@class,'save-button-wrap')]/button")
    CHECK_CREATED_CAMPAIGN_LOCATOR = (By.XPATH, "//input[contains(@class, 'nameCell-module-checkbox')]")
    SEARCH_CANPAIGN_FLD_LOCATOR = (By.XPATH, "//input[contains(@class, 'multiSelectSuggester-module-searchInput')]")
    NO_CAMPAIGN_FOUND_LOCATOR = (By.XPATH, "//span[contains(@class, 'suggesterOptionsList-module-emptyItem')]")
    FOUND_CAMPAGN_LOCATOR = (By.XPATH, "//li[@title='{}']")
    ACTIONS_CAMPAIGN_BTN_LOCATOR = (By.XPATH, "//div[contains(@class, 'tableControls-module-massActionsSelect')]")
    DELETE_CAMPAIGN_BTN_LOCATOR = (By.XPATH, "//ul[contains(@class, 'optionsList-module-optionsList')]/li[6]")

class AudiencePageLocators(BasePageLocators):
    CREATE_SEGMENT_BTN_LOCATOR = (By.XPATH, "//div[contains(@class,'create-button')]/button")
    CREATE_SEGMENT_ONBOARDING_BTN_LOCATOR = (By.XPATH, "//a[contains(@href,'segments/segments_list/new')]")
    GROUPS_BTN_LOCATOR = (By.XPATH, "// div[contains(@class, 'left-nav__item')]/a[@href='/segments/groups_list']")
    LINK_GROUPS_INPUT_FLD_LOCATOR = (By.XPATH, "//input[contains(@class, 'multiSelectSuggester-module-searchInput')]")
    SHOW_BTN_LOCATOR = (By.XPATH, "//div[contains(@class, 'optionListTitle-module-control') and @data-test='show']")
    VK_EDU_BTN_LOCATOR = (By.XPATH, "//ul[contains(@class, 'optionsList-module-list')]/li[@title='VK Образование']")
    ADD_SELCTED_BTN_LOCATOR = (By.XPATH, "//div[@data-test='add_selected_items_button']")
    GROUPS_VK_OK_IN_LIST_BTN_LOCATOR = (By.XPATH, "//div[contains(@class, 'js-sources-types')]/div[10]")
    PUT_CHECK_BTN_LOCATOR = (By.XPATH, "//input[contains(@class, 'main-source-checkbox')]")
    ADD_SEGMENT_BTN_LOCATOR = (By.XPATH, "//div[contains(@class, 'add-button')]/button")
    APPROVE_CREATE_SEGMENT_BTN_LOCATOR = (By.XPATH, "//button[contains(@class, 'button button_submit')]")
    FIND_CREATED_SEGMENT_FLD_LOCATOR = (By.XPATH, "//input[contains(@class, 'suggester-module-searchInput')]")
    NO_SEGMENT_FOUND_LOCATOR = (By.XPATH, "//li[contains(@class, 'optionsList-module-optionNothing')]")
    FOUND_SEGMENT_LOCATOR = (By.XPATH, "//li[@title='{}']")
    CHECK_CREATED_SEGMENT_LOCATOR = (By.XPATH, "//div[contains(@class, 'segmentsTable-module-idCellWrap')]/input")
    ACTIONS_BTN_LOCATOR = (By.XPATH, "//div[contains(@class, 'segmentsTable-module-massActionsSelect')]")
    SEGMENT_NAME_FIELD_LOCATOR = (By.XPATH, "//div[contains(@class, 'input input_create-segment-form')]/div/input")
    DELETE_AUD_SEG_BTN_LOCATOR = (By.XPATH, "//ul[contains(@class, 'optionsList-module-optionsList')]")
    DELETE_SOURCE_BTN = (By.XPATH, "//td[contains(@class, 'js-cell-group-remove')]/div")
    CONFIRM_DELETE_BTN_LOCATOR = (By.XPATH, "//button[contains(@class, 'button button_confirm-remove')]")
