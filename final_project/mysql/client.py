import sqlalchemy
from sqlalchemy.orm import sessionmaker

from mysql.model import UsersTable

class MysqlClient:
    def __init__(self, db_name, user, password, host='127.0.0.1', port=3306):
        self.user = user
        self.port = port
        self.password = password
        self.host = host
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()
