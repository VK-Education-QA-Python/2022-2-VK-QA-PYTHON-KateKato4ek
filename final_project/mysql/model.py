from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class UsersTable(Base):
    __tablename__ = 'test_users'
    __table_arg__ = {'mysql_charset': 'utf8'}
    
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    username = Column(String(16), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=True, unique=True)
    access = Column(Integer, nullable=True)
    active = Column(Integer, nullable=True)
    start_active_time = Column(DateTime, nullable=True)
