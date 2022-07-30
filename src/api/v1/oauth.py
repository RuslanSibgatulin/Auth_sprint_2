from http import HTTPStatus

from authlib.integrations.flask_client import OAuth
from flask import Blueprint
from flask import current_app as app
from flask import request
from flask_restful import Api

from api.base import BaseView
from config import settings
from db.controllers.users import UserController
from db.redis import TokenStorage
from utils import Proveiders, SocialUserPayload, TokenMaker

oauth = OAuth(app)

oauth_blueprint = Blueprint("oauth", __name__)
api = Api(oauth_blueprint)

access_data = {
    "grant_type": "authorization_code",
    "client_id": settings.YANDEX_CLIENT_ID,
    "client_secret": settings.YANDEX_CLIENT_SECRET,
}

oauth.register(
    Proveiders.YANDEX.value,
    client_id=settings.YANDEX_CLIENT_ID,
    client_secret=settings.YANDEX_CLIENT_SECRET,
    base_url="https://oauth.yandex.ru/",
    access_token_params=access_data,
    authorize_url="https://oauth.yandex.ru/authorize",
    access_token_url="https://oauth.yandex.ru/token",
    userinfo_endpoint="https://login.yandex.ru/info",
)


class YandexLogin(BaseView):
    def get(self, provider: str):
        oauth_provider = oauth.create_client(provider)
        if oauth_provider is None:
            return {"message": f"Error! Wrong client - {provider}."}, HTTPStatus.BAD_REQUEST
        return oauth_provider.authorize_redirect(settings.YANDEX_REDIRECT_URL)


class YandexCallbackView(BaseView):
    def get(self, provider: str):
        oauth_provider = oauth.create_client(provider)
        oauth_provider.authorize_access_token()
        userinfo = oauth_provider.userinfo()
        payload = SocialUserPayload(
            social_id=userinfo["id"], login=userinfo["login"], email=userinfo["default_email"], social_name=provider
        )
        controller = UserController()
        user = controller.create_social_user(payload)
        agent = request.user_agent
        access_token, refresh_token = TokenMaker.create_tokens_pair(user)
        TokenStorage().add_token_pair(
            user_id=user.id, user_agent=agent.string, refresh_token=refresh_token, access_token=access_token
        )
        controller.add_login_record(dict(user_id=user.id, platform=agent.platform, ip=request.remote_addr))
        return {"access_token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK


api.add_resource(YandexLogin, "/v1/oauth/login/<string:provider>")
api.add_resource(YandexCallbackView, "/v1/oauth/callback/<string:provider>")
