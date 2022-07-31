from pydantic import BaseModel

from utils.exceptions import CreationError
from utils.password import PasswordHasher


class BaseUser(BaseModel):
    login: str


class LoginUser(BaseUser):
    password: str


class CreateUser(LoginUser):
    second_password: str
    email: str

    def __init__(self, **kwargs):
        super(CreateUser, self).__init__(**kwargs)
        if self.password != self.second_password:
            raise CreationError
        new_password = PasswordHasher.hash_password(self.password)
        self.password = new_password
        self.second_password = new_password

    def get_payload(self) -> dict[str, str]:
        return dict(password_hash=self.password, login=self.login, email=self.email)


class UserHistory(BaseUser):
    history: list[str]
