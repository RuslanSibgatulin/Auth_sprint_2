from utils.exceptions import OAuthEmailError
from utils.oauth.enums import SocialPoviders
from utils.oauth.payload import SocialUserPayload
from utils.oauth.providers.base import BaseProviderService


class VKProviderService(BaseProviderService):
    NAME = SocialPoviders.VK.value

    @classmethod
    def get_userinfo(cls, userinfo: dict, token: dict) -> SocialUserPayload:
        user_data = userinfo.get("response")[0]
        email = token.get("email")
        if email is None:
            raise OAuthEmailError
        return SocialUserPayload(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            social_id=user_data["id"],
            login=user_data.get("screen_name") or token.get("email"),
            email=token.get("email") or user_data.get("screen_name"),
            social_name=cls.NAME,
        )
