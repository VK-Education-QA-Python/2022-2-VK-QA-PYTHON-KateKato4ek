import sqlalchemy
from sqlalchemy.orm import sessionmaker

from model import Base

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

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()
    
    def create_tables(self):
        tables = [
            'common_amount_of_requests',
            'requests_amount_by_types',
            'most_frequent_requests',
            'most_frecuent_requests_with_4XX_status_code',
            'users_by_requests_with_5XX_status_code',
        ]
        
        for table in tables:
            if not sqlalchemy.inspect(self.engine).has_table(table):
                Base.metadata.tables[table].create(self.engine)
