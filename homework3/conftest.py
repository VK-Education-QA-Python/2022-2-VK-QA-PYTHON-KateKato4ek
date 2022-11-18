import os
import shutil
import sys
import logging

import pytest

from api.client import ApiClient
from fixtures import *

def pytest_addoption(parser):
    parser.addoption("--url", default="https://target-sandbox.my.com/")
    parser.addoption('--debug_log', action='store_true')

@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    debug_log = request.config.getoption('--debug_log')

    return {
        'url': url,
        'debug_log': debug_log,
    }

@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))

@pytest.fixture(scope='session')
def base_temp_dir():
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    return base_dir

@pytest.fixture(scope='function')
def temp_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    temp_dir = os.path.join(request.config.base_temp_dir, test_name)
    os.makedirs(temp_dir)
    return temp_dir

@pytest.fixture(scope='function')
def logger(temp_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

@pytest.fixture(scope='session')
def api_client(credentials, repo_root, config):
    return ApiClient(base_url=config['url'],
                     login=credentials[0],
                     password=credentials[1],
                     repo_root=repo_root)
