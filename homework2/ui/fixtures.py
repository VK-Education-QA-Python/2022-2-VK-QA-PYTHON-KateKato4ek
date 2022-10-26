import os
import sys
import shutil

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
from numpy import random
from PIL import Image

from ui.pages.main_page import MainPage
from ui.utils.utils import random_string

def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir

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
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    
    driver.get(url)
    driver.set_window_size(1400, 800)
    
    yield driver
    
    driver.quit()

def get_driver(browser_name):
    if browser_name == 'chrome':
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif browser_name == 'firefox':
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
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

    return user, password

@pytest.fixture(scope='session')
def cookies(credentials, config):
    driver = get_driver(config['browser'])
    driver.get(config['url'])
    main_page = MainPage(driver)
    main_page.login(*credentials)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies

@pytest.fixture(scope='function')
def temp_image(temp_dir):
    pic_array = random.rand(400, 240, 3) * 255
    pic = Image.fromarray(pic_array.astype('uint8')).convert('L')
    pic_name = random_string() + '.png'
    path = os.path.join(temp_dir, pic_name)
    pic.save(path)
    return path
