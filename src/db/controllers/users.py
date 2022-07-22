from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.query import Query

from db.base import db_session
from db.models import LoginHistory, User, UserRole


class UserController:
    MODEL = User
    SEARCH_FIELD = "login"
    DEFAULT_ROLE_ID = 1

    def create(self, payload: dict, role_id: int = None) -> None:
        new_user = self.MODEL(**payload)
        new_user_role = UserRole(user=new_user, role_id=role_id or self.DEFAULT_ROLE_ID)
        db_session.add(new_user)
        db_session.add(new_user_role)
        try:
            db_session.flush()
        except IntegrityError as e:
            db_session.rollback()
            raise e
        db_session.commit()

    def update(self, user: User, payload: dict) -> None:
        for key, value in payload.items():
            setattr(user, key, value)
        db_session.add(user)
        try:
            db_session.flush()
        except IntegrityError as e:
            db_session.rollback()
            raise e
        db_session.commit()

    def get_by_login(self, payload: str) -> User:
        user = db_session.query(self.MODEL).filter_by(login=payload).first()
        db_session.commit()
        return user

    def get_by_id(self, payload: str) -> User:
        user = db_session.query(self.MODEL).filter_by(id=payload).first()
        db_session.commit()
        return user

    def get_user_history(self, payload: str, skip: int = 1, limit: int = 5) -> list[dict]:
        query: Query = db_session.query(LoginHistory)
        logins = query.filter_by(user_id=payload).order_by(LoginHistory.login_at.desc()).limit(limit).offset(skip)
        history = list()
        for login in logins:
            obj_ = dict(platform=login.platform, login_at=str(login.login_at), ip=login.ip)
            history.append(obj_)
        return history

    def add_login_record(self, payload: dict) -> None:
        new_obj = LoginHistory(**payload)
        db_session.add(new_obj)
        db_session.commit()
