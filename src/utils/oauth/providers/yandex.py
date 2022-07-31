from utils.oauth.enums import SocialPoviders
from utils.oauth.payload import SocialUserPayload
from utils.oauth.providers.base import BaseProviderService


class YandexProviderService(BaseProviderService):
    NAME = SocialPoviders.YANDEX.value

    @classmethod
    def get_userinfo(cls, userinfo: dict, token: dict) -> SocialUserPayload:
        login_field = userinfo["login"]
        login = login_field.split("@")[0] if "@" in login_field else login_field
        return SocialUserPayload(
            first_name=userinfo["first_name"],
            last_name=userinfo["last_name"],
            social_id=userinfo["id"],
            login=login,
            email=userinfo["default_email"],
            social_name=cls.NAME,
        )
