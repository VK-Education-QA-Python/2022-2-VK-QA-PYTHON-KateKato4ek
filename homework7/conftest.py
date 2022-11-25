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
