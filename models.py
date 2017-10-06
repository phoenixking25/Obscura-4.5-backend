from sqlalchemy import Column, UniqueConstraint, create_engine
from sqlalchemy import Integer, ForeignKey, String, TypeDecorator, Unicode, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, \
     check_password_hash

import config


engine = create_engine(config.mysql['CREATE_ENGINE_URL'], echo=True)
DeclarativeBase = declarative_base(engine)
metadata = DeclarativeBase.metadata

class Player(DeclarativeBase):
    __tablename__ = 'Player'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    email = Column(String(200))
    username = Column(String(200))
    college = Column(String(200))
    phone = Column(String(200))
    level = Column(String(200))
    levelId = Column(Integer)
    picture = Column(String(200))
    time = Column(DateTime)

    def __init__(self, name=None, email=None, username=None, college=None, phone=None, level=None, levelId=None, picture=None):
        self.name = name 
        self.email = email
        self.username = username
        self.college = college
        self.phone = phone
        self.level = level
        self.levelId = levelId
        self.picture = picture

    def __repr__(self):
        return self.username


class Level(DeclarativeBase):
    __tablename__ = 'Level'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    levelNo = Column(Integer)
    d_name = Column(String(500))
    picture = Column(String(500))
    html = Column(String(200))
    js = Column(String(500))
    hint = Column(String(500))
    ans = Column(String(500))
    

    def __init__(self, name=None, levelNo=None, nextUrl=None, picture=None, html=None, js=None, hint=None, ans=None):
        self.name = name
        self.levelNo = levelNo
        self.nextUrl = nextUrl
        self.picture = picture
        self.html = html
        self.js = js
        self.hint = hint
        self.ans = ans

    def __repr__(self):
        return self.name



metadata.create_all()
