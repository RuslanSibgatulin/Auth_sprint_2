from abc import ABC, abstractmethod
from typing import Any

from authlib.integrations.flask_client.apps import FlaskOAuth2App

from utils.oauth.app import oauth
from utils.oauth.payload import SocialUserPayload


class ProviderService(ABC):
    NAME: str = None

    @abstractmethod
    def get_proveider(self) -> FlaskOAuth2App:
        ...

    @abstractmethod
    def get_userinfo(self, userinfo: dict, token: dict) -> SocialUserPayload:
        ...

    @abstractmethod
    def get_user_payload(self) -> SocialUserPayload:
        ...


class BaseProviderService(ProviderService):
    @classmethod
    def get_proveider(cls) -> Any:
        oauth_provider = oauth.create_client(cls.NAME)
        return oauth_provider

    @classmethod
    def get_user_payload(cls) -> SocialUserPayload:
        oauth_provider = cls.get_proveider()
        token = oauth_provider.authorize_access_token()
        userinfo = oauth_provider.userinfo()
        user_payload = cls.get_userinfo(userinfo, token)
        return user_payload

    @classmethod
    def get_userinfo(cls, userinfo: dict, token: dict) -> SocialUserPayload:
        pass
