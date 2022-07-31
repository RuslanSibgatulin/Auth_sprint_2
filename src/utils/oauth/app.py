from authlib.integrations.flask_client import OAuth
from flask import current_app as app

from config import settings
from utils.oauth.enums import SocialPoviders

oauth = OAuth(app)
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
    userinfo_endpoint="https://api.vk.com/method/{0}?v={1}&fields={2}".format("users.get", 5.131, "screen_name"),
)
