from enum import Enum, unique


@unique
class SocialPoviders(Enum):
    YANDEX = "yandex"
    VK = "vk"
    GOOGLE = "google"
    MAIL = "mail"
    FACEBOOK = "facebook"
