from sqlalchemy.exc import IntegrityError

from db import models as models
from db.base import db_session
from db.controllers.exceptions import AlreadyExistsError, NotFoundError
from models.user_role import UserRole, UserRoleCreate, UserRoleDelete


class UserRoleController:
    MODEL = models.UserRole

    @classmethod
    def create(cls, user_role: UserRoleCreate) -> UserRole:
        user_role_obj = cls.MODEL(user_id=user_role.user_id, role_id=user_role.role_id)
        try:
            db_session.add(user_role_obj)
            db_session.commit()
            db_session.refresh(user_role_obj)
            user_role_res = UserRole.from_orm(user_role_obj)
            user_role_res.user_id = str(user_role_res)
            return user_role_res
        except IntegrityError:
            raise AlreadyExistsError()

    @classmethod
    def remove(cls, user_role: UserRoleDelete) -> UserRole:
        user_role_obj = (
            db_session.query(cls.MODEL)
            .filter((cls.MODEL.user_id == user_role.user_id) & (cls.MODEL.role_id == user_role.role_id))
            .first()
        )
        if not user_role_obj:
            raise NotFoundError
        db_session.delete(user_role_obj)
        db_session.commit()
        user_role_res = UserRole.from_orm(user_role_obj)
        user_role_res.user_id = str(user_role_res)
        return user_role_res
