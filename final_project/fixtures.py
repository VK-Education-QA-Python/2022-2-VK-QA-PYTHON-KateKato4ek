import os

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from ui.pages.login_page import LoginPage

@pytest.fixture(scope='function')
def driver(config, temp_dir):
    browser = config['browser']
    url = config['url']
    headless = config["headless"]
    selenoid = config['selenoid']
    vnc = config['vnc']
    
    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": temp_dir})
    if headless:
        options.add_argument("--headless")
    
    if selenoid:
        capabilities = {
            'browserName': 'chrome',
            'version': '106.0',
        }
        if vnc:
            capabilities['enableVNC'] = True
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    elif browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    
    driver.get(url)
    driver.set_window_size(1400, 800)
    
    yield driver
    
    driver.quit()

def get_driver(browser_name):
    if browser_name == 'chrome':
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser_name}"')
    browser.set_window_size(1400, 800)
    
    return browser

@pytest.fixture(scope='session')
def credentials(repo_root, file_name='creds'):
    cred_path = os.path.join(repo_root, file_name)
    with open(cred_path, 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
        email = f.readline().strip()

    return user, password, email

@pytest.fixture(scope='session')
def cookies(credentials, config):
    driver = get_driver(config['browser'])
    driver.get(config['url'])
    login_page = LoginPage(driver)
    login_page.login(username=credentials[0], password=credentials[1])

    cookies = driver.get_cookies()
    driver.quit()
    return cookies
