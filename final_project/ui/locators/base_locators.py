from selenium.webdriver.common.by import By

class BasePageLocators:
    pass

class LoginPageLocators(BasePageLocators):
    FIELD_TEMPLATE_REQUIRED = (By.XPATH, "//input[@id='{}' and @required]")
    USERNAME_FIELD = (By.XPATH, "//input[@id='username' and @required]")
    PASSWORD_FIELD = (By.XPATH, "//input[@id='password' and @required]")
    LOGIN_BUTTON = (By.ID, "submit")
    CREATE_ACCOUNT_LINK = (By.XPATH, "//div/a/..")
    INVALID_USERNAME_OR_PASSWORD_WARNING = (By.XPATH, "//div[@id='flash' and 'Invalid username or password']")
    BLOCKED_ACCOUNT_WARNING = (By.XPATH, "//div[@id='flash' and 'Ваша учетная запись заблокирована']")
    
class RegisterPageLocators(BasePageLocators):
    FIELD_TEMPLATE_REQUIRED = (By.XPATH, "//input[@id='{}' and @required]")
    FIELD_TEMPLATE = (By.XPATH, "//input[@id='{}']")
    NAME_FIELD = (By.XPATH, "//input[@id='user_name' and @required]")
    SURNAME_FIELD = (By.XPATH, "//input[@id='user_surname' and @required]")
    MIDDLENAME_FIELD = (By.ID, "user_middle_name")
    USERNAME_FIELD = (By.XPATH, "//input[@id='username' and @required]")
    EMAIL_FIELD = (By.ID, "email")
    VALID_EMAIL_FIELD = (By.XPATH, "//input[@id='email' and @required]")
    PASSWORD_FIELD = (By.XPATH, "//input[@id='password' and @required]")
    VALID_CONFIRMPASSWORD_FIELD = (By.XPATH, "//input[@id='confirm' and @required]")
    CONFIRMPASSWORD_FIELD = (By.ID, "confirm")
    CHECKBOX = (By.XPATH, "//input[@id='term' and @required]")
    REGISTER_BUTTON = (By.ID, "submit")
    LOGIN_IN_LINK = (By.XPATH, "//div/a/..")
    WARNING_MESSAGE = (By.XPATH, "//div[@id='flash' and 'Invalid email address' and 'Passwords must match']")
    USER_EXISTS_WARNING = (By.XPATH, "//div[@id='flash' and 'User already exist']")

class HomePageLocators(BasePageLocators):
    HOME_BTN = (By.XPATH, "//ul[contains(@class, 'uk-navbar-nav')]/li/a")
    AUDIENCE_BTN_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-segments')]")
    LOG_OUT_BTN = (By.ID, "logout")
    CENTRAL_CIRCLE_BTN = (By.XPATH, "//div[contains(@class, 'uk-width-1-3')]/div[contains(text(), '{}')]/../figure")
    PYTHON_FACT = (By.XPATH, "//footer/div/p")
    VK_ID = (By.XPATH, "//div[@id='login-name']/ul/li[3]")
