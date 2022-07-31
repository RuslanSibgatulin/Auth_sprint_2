from enum import Enum, unique
from http import HTTPStatus

from api.base import BaseView
from authlib.integrations.flask_client import OAuth
from config import settings
from db.controllers.users import UserController
from db.redis import TokenStorage

from flask import Blueprint, url_for
from flask import current_app as app
from flask import request
from flask_restful import Api
from utils import SocialUserPayload, TokenMaker

oauth = OAuth(app)

oauth_blueprint = Blueprint("oauth", __name__)
api = Api(oauth_blueprint)


@unique
class SocialPoviders(Enum):
    YANDEX = "yandex"
    VK = "vk"
    GOOGLE = "google"
    MAIL = "mail"
    FACEBOOK = "facebook"


oauth.register(
    SocialPoviders.YANDEX.value,
    client_id=settings.YANDEX_CLIENT_ID,
    client_secret=settings.YANDEX_CLIENT_SECRET,
    base_url="https://oauth.yandex.ru/",
    access_token_params={
        "grant_type": "authorization_code",
        "client_id": settings.YANDEX_CLIENT_ID,
        "client_secret": settings.YANDEX_CLIENT_SECRET,
    },
    authorize_url="https://oauth.yandex.ru/authorize",
    access_token_url="https://oauth.yandex.ru/token",
    userinfo_endpoint="https://login.yandex.ru/info",
)

oauth.register(
    SocialPoviders.VK.value,
    client_id=settings.VK_APP_ID,
    client_secret=settings.VK_APP_SECURE_KEY,
    authorize_params={"scope": "email"},
    authorize_url="https://oauth.vk.com/authorize",
    access_token_url="https://oauth.vk.com/access_token",
    access_token_params={
        "grant_type": "authorization_code",
        "client_id": settings.VK_APP_ID,
        "client_secret": settings.VK_APP_SECURE_KEY,
        "display": "page",
    },
    access_token_method="GET",
    userinfo_endpoint="https://api.vk.com/method/{0}?v={1}&fields={2}".format(
        "users.get", 5.131, "screen_name"
    ),
)


class SocialLogin(BaseView):
    def get(self, provider: str):
        oauth_provider = oauth.create_client(provider)
        if oauth_provider is None:
            return {
                "message": f"Wrong OAuth provider - {provider}."
            }, HTTPStatus.BAD_REQUEST
        return oauth_provider.authorize_redirect(
            url_for(".socialcallbackview", provider=provider, _external=True)
        )


class SocialCallbackView(BaseView):
    def get(self, provider: str):
        oauth_provider = oauth.create_client(provider)
        token = oauth_provider.authorize_access_token()
        userinfo = oauth_provider.userinfo()
        payload = self.getUser(provider, userinfo, token)
        controller = UserController()
        user = controller.create_social_user(payload)
        agent = request.user_agent
        access_token, refresh_token = TokenMaker.create_tokens_pair(user)
        TokenStorage().add_token_pair(
            user_id=user.id,
            user_agent=agent.string,
            refresh_token=refresh_token,
            access_token=access_token,
        )
        controller.add_login_record(
            dict(user_id=user.id, platform=agent.platform, ip=request.remote_addr)
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, HTTPStatus.OK

    @staticmethod
    def getUser(
        provider: str, userinfo: dict, token: dict
    ) -> SocialUserPayload:
        if provider == SocialPoviders.YANDEX.value:
            return SocialUserPayload(
                first_name=userinfo["first_name"],
                last_name=userinfo["last_name"],
                social_id=userinfo["id"],
                login=userinfo["login"],
                email=userinfo["default_email"],
                social_name=provider,
            )
        elif provider == SocialPoviders.VK.value:
            user_data = userinfo.get("response")[0]
            return SocialUserPayload(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                social_id=user_data["id"],
                login=user_data.get("screen_name") or token["email"],
                email=token["email"],
                social_name=provider,
            )


api.add_resource(SocialLogin, "/v1/oauth/login/<string:provider>")
api.add_resource(SocialCallbackView, "/v1/oauth/callback/<string:provider>")
