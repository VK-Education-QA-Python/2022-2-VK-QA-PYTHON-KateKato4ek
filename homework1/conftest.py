import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--url", default="https://target-sandbox.my.com/")
    parser.addoption('--headless', action='store_true')

@pytest.fixture()
def config(request):
    browser = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    headless = request.config.getoption("--headless")
    return {"browser": browser, "url": url, "headless": headless}

@pytest.fixture(scope='function')
def driver(config):
    browser = config["browser"]
    url = config["url"]
    headless = config["headless"]
    
    options = Options()
    if headless:
        options.add_argument("--headless")

    if browser == "chrome":
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')

    driver.get(url)
    driver.set_window_size(1200, 600)
    yield driver
    driver.quit()
