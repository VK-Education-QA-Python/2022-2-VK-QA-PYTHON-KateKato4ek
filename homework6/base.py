import pytest

from client import MysqlClient
from builder import MysqlBuilder

class BaseTest(object):
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, parser):
        self.mysql_client: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(client=mysql_client, parser=parser)

    def get_rows_count(self, table):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(table).count()
