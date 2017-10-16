import config as config
from flask_api import FlaskAPI
from routes import obscura
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from flask_cors import CORS, cross_origin

#author : anuj(phoenixking25)
#obscura_version: 4.5

app = FlaskAPI(__name__)
CORS(app)

def run():
    app.register_blueprint(obscura)
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=False, processes=1)

if __name__ == '__main__':
    run()
