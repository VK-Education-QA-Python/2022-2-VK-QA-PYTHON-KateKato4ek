from selenium.webdriver.common.by import By

LOGIN_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")
EMAIL_INPUT_LOCATOR = (By.XPATH, "//input[contains(@class, 'authForm-module-input') and @name='email']")
PASWORD_INPUT_LOCATOR = (By.XPATH, "//input[contains(@class, 'authForm-module-inputPassword') and @name='password']")
SEND_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'authForm-module-button')]")
ACCOUNT_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'right-module-rightButton')]")
LOGOUT_BUUTTON_LOCATOR = (By.XPATH, "//ul[contains(@class, 'rightMenu-module-shownRightMenu')]/li[2]")
PROFILE_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-profile')]")
NAME_FIELD_LOCATOR = (By.XPATH, "//div[@data-name='fio']/div/input")
SAVE_BUTTON_LOCATOR = (By.XPATH, "//button[@data-class-name='Submit']")
TOOLS_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-tools')]")
LIST_OF_FIDS_LOCATOR = (By.XPATH, "//div[contains(@class, 'feeds-module-title')]")
