import hashlib

from config import settings


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
