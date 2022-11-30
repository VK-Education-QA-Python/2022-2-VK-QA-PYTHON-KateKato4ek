from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class UniqRequestsCountTable(Base):
    __tablename__ = 'common_amount_of_requests'
    __table_arg__ = {'mysql_charset': 'utf8'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=False)
    
class AmountOfRequestsByTypeTable(Base):
    __tablename__ = 'requests_amount_by_types'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(512), nullable=False)
    count = Column(Integer, nullable=False)
    
class MostFrequentRequestsTable(Base):
    __tablename__ = 'most_frequent_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(512), nullable=False)
    count = Column(Integer, nullable=False)
    
class MostFrequent4XXRequestsTable(Base):
    __tablename__ = 'most_frecuent_requests_with_4XX_status_code'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    status = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    url = Column(String(512), nullable=False)
    
class MostFrequent5XXRequestsByIpTable(Base):
    __tablename__ = 'users_by_requests_with_5XX_status_code'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    count = Column(Integer, nullable=False)
