import enum
import hashlib
import string
from dataclasses import dataclass
from secrets import choice

from flask_jwt_extended import create_access_token, create_refresh_token

from config import settings
from db.models import User


class CreationError(Exception):
    pass


class PasswordHasher:
    SALT = settings.PASSWORD_SALT
    ALGORITHM = settings.HASH_ALGORITHM

    @classmethod
    def hash_password(cls, password: str) -> str:
        hashed_password = hashlib.pbkdf2_hmac(
            cls.ALGORITHM, password.encode("utf-8"), cls.SALT.encode("utf-8"), 100000
        )
        return hashed_password.hex()

    @classmethod
    def check_password(cls, password: str, hashed_password: str) -> bool:
        new_hashed_password = cls.hash_password(password)
        return hashed_password == new_hashed_password

    @classmethod
    def generate_password(cls) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(choice(alphabet) for _ in range(16))


@dataclass
class SocialUserPayload:
    social_id: str
    login: str
    email: str
    social_name: str


class Proveiders(enum.Enum):
    YANDEX = "yandex"


class TokenMaker:
    @classmethod
    def create_tokens_pair(cls, user: User) -> tuple[str, str]:
        action_ids = set([action.id for user_role in user.roles for action in user_role.role.actions])
        access_token = create_access_token({"user_id": user.id, "action_ids": list(action_ids)})
        refresh_token = create_refresh_token({"user_id": user.id})
        return access_token, refresh_token
