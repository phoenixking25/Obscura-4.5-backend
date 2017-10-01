from sqlalchemy import create_engine, Index
from sqlalchemy.orm import sessionmaker, scoped_session
from models import  DeclarativeBase
import config

class DatabaseHandler:
    def __init__(self):
        pass

    @staticmethod
    def connect_to_database():
        """
        Connect to our SQLite database and return a Session object
        """

        engine = create_engine(config.sqlite['CREATE_ENGINE_URL'], echo=True)
        engine.raw_connection().connection.text_factory = lambda x: x.encode('utf-8', 'ignore')
        session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
        DeclarativeBase.query = session.query_property()
        return session()