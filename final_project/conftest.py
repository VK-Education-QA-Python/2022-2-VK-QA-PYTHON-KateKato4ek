import os
import shutil
import sys
import logging

import pytest

from api.client import ApiClient
from mysql.client import MysqlClient
from fixtures import *
from mysql.builder import MysqlBuilder

def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--url", default="http://127.0.0.1:8083")
    parser.addoption('--headless', action='store_true')
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')

@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')
    headless = request.config.getoption("--headless")
    debug_log = request.config.getoption('--debug_log')
    
    if request.config.getoption('--selenoid'):
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
        selenoid = 'http://127.0.0.1:4444/wd/hub'
    else:
        selenoid = None
        vnc = False

    return {
        'browser': browser,
        'url': url,
        "headless": headless,
        'debug_log': debug_log,
        'selenoid': selenoid,
        'vnc': vnc,
    }

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
    
    mysql_client = MysqlClient(user='test_qa', password='qa_test', db_name='vkeducation')
    mysql_client.connect(db_created=True)
    config.mysql_client = mysql_client

@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()

@pytest.fixture(scope='function')
def mysql_builder(mysql_client):
    return MysqlBuilder(client=mysql_client)

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
                     username=credentials[0],
                     password=credentials[1],
                     repo_root=repo_root)