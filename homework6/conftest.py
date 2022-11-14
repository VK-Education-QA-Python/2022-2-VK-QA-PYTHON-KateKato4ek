import pytest
from client import MysqlClient
from parser import Parser

def pytest_addoption(parser):
    parser.addoption('--path', default='./homework6/access.logs')

def pytest_configure(config):
    path = config.getoption('--path')
    parser = Parser(path)
    
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_tables()

    config.mysql_client = mysql_client
    config.parser = parser

@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()

@pytest.fixture(scope='session')
def parser(request) -> Parser:
    parser: Parser = request.config.parser
    parser.parse_log_file()
    return parser
