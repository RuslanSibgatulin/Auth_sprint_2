from dataclasses import dataclass


@dataclass
class SocialUserPayload:
    first_name: str
    last_name: str
    social_id: str
    login: str
    email: str
    social_name: str
