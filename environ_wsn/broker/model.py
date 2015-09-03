from dateutil.parser import parse
from sqlalchemy import Integer, Column, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import SQLITE_TEST_DB

__author__ = 'laurogama'

Base = declarative_base()
engine = create_engine(SQLITE_TEST_DB)

def create_db():
    Base.metadata.create_all(engine)
    return True


def clean_db():
    Base.metadata.drop_all(bind=engine)


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)

def create_db_session():
    if create_db():
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        return DBSession()
    return None

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    sender = Column(Integer)
    temperature = Column(Integer)
    humidity = Column(Integer)
    noise = Column(Integer)
    luminance = Column(Integer)
    gas = Column(Integer)

    def __init__(self, message):
        try:
            self.timestamp = parse(message['timestamp'])
            self.sender = message['id']
            self.humidity = message['data']['humidity']
            self.luminance = message['data']['luminance']
            self.temperature = message['data']['temperature']
            self.noise = message['data']['noise']
            self.gas = message['data']['gas']
        except:
            raise

    def __repr__(self):
        return "Message {} from {}, at {} ".format(self.id, self.sender,
                                                   self.timestamp)
