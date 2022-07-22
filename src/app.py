from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from api.v1.actions import action_blueprint
from api.v1.oauth import oauth_blueprint
from api.v1.roles import role_blueprint
from api.v1.users import user_blueprint
from config import settings
from db.base import init_db

app = Flask(__name__)
app.config.from_object(settings)
api = Api(app=app)
jwt = JWTManager(app)

app.register_blueprint(action_blueprint)
app.register_blueprint(oauth_blueprint)
app.register_blueprint(role_blueprint)
app.register_blueprint(user_blueprint)

app.config["SWAGGER"] = {
    "specs": [
        {
            "endpoint": '/apidocs/apispec_1',
            "route": '/apidocs/apispec_1.json'
        }
    ],
    "static_url_path": "/apidocs/flasgger_static",
    "specs_route": "/apidocs/"
}
swagger = Swagger(app, template_file='apidocs/swagger.json')


init_db()


def main():
    app.run(debug=True, port=8000)


if __name__ == "__main__":
    main()
