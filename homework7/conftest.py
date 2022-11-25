import os
import shutil
import sys
import logging
import pytest

from waiter import Waiter
from settings import APP_HOST, APP_PORT, MOCK_HOST, MOCK_PORT
import flask_mock
import app

def pytest_configure(config):
    if hasattr(config, 'workerinput'):
        return
    
    config.app_server = app.run()
    Waiter.wait_ready(APP_HOST, APP_PORT)
    
    config.mock_server = flask_mock.run()
    Waiter.wait_ready(MOCK_HOST, MOCK_PORT)

def pytest_unconfigure(config):
    config.app_server.shutdown()
    config.mock_server.shutdown()

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
    temp_dir = os.path.join(base_temp_dir(), test_name)
    os.makedirs(temp_dir)
    
    return temp_dir

@pytest.fixture(scope='function', autouse=True)
def logger(temp_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.DEBUG

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False # !
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()
