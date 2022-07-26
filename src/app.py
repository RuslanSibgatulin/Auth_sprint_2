from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api

from api.v1.actions import action_blueprint
from api.v1.oauth import oauth_blueprint
from api.v1.roles import role_blueprint
from api.v1.users import user_blueprint
from config import settings
from tracer.jaeger import tracer_init

app = Flask(__name__)
app.config.from_object(settings)
api = Api(app=app)
jwt = JWTManager(app)
limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["200 per day", "10 per hour"], storage_uri=settings.redis_uri
)
app.register_blueprint(action_blueprint)
app.register_blueprint(oauth_blueprint)
app.register_blueprint(role_blueprint)
app.register_blueprint(user_blueprint)

app.config["SWAGGER"] = {
    "specs": [{"endpoint": "/apidocs/apispec_1", "route": "/apidocs/apispec_1.json"}],
    "static_url_path": "/apidocs/flasgger_static",
    "specs_route": "/apidocs/",
}

swagger = Swagger(app, template_file="apidocs/swagger.json")

tracer_init(app)