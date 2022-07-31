from utils.oauth.enums import SocialPoviders
from utils.oauth.providers.base import ProviderService
from utils.oauth.providers.vk import VKProviderService
from utils.oauth.providers.yandex import YandexProviderService


class ProviderFactory:
    SEVICES: dict[str, ProviderService] = {
        SocialPoviders.VK.value: VKProviderService,
        SocialPoviders.YANDEX.value: YandexProviderService,
    }

    @classmethod
    def get_service(cls, name: str) -> ProviderService:
        return cls.SEVICES.get(name)
