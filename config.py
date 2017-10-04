import config_global as global_file
HOST = '0.0.0.0'
PORT = 8080
SQLALCHEMY_DATABASE_URI = global_file.database_url
SQLALCHEMY_TRACK_MODIFICATIONS = False
PASS_SECRET = 'phoenix'
mysql = {
    'CREATE_ENGINE_URL': global_file.database_url
}
JWT_SECRET = global_file.secret_key

#mysql+pymysql://root:password@host/db_name