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

from api.utils import random_string

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

@pytest.fixture(scope='session')
def credentials(repo_root, file_name='creds'):
    cred_path = os.path.join(repo_root, file_name)
    with open(cred_path, 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()

    return user, password

@pytest.fixture(scope='function')
def temp_image(temp_dir):
    pic_array = random.rand(400, 240, 3) * 255
    pic = Image.fromarray(pic_array.astype('uint8')).convert('L')
    pic_name = random_string() + '.png'
    path = os.path.join(temp_dir, pic_name)
    pic.save(path)
    return path
