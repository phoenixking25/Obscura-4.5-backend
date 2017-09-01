import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'obscura.db')
SECRET_KEY = 'obscura'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET = 'rutherford1992'
DEBUG = True
HOST = '0.0.0.0'
PORT = 8080
sqlite = {
    'CREATE_ENGINE_URL': 'sqlite:///{}'.format(DB_PATH)
}