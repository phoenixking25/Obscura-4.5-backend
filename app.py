import config as config
from flask_api import FlaskAPI
from routes import obscura
from routes import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from flask_cors import CORS, cross_origin

app = FlaskAPI(__name__)
CORS(app)

jwt = JWT(app, authenticate, identity)

def run():
    app.register_blueprint(obscura)
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=False, processes=1)


if __name__ == '__main__':
    run()
