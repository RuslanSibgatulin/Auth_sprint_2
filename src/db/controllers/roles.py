from typing import Optional

import models.roles as schemas
from db import models as models
from db.base import db_session
from db.models import Action, Role


class RoleController:
    MODEL = models.Role

    @classmethod
    def create(cls, role: schemas.RoleCreate) -> schemas.Role:
        role_obj = cls.MODEL(name=role.name)

        for action in role.actions:
            role_obj.actions.append(action)

        db_session.add(role_obj)
        db_session.commit()
        db_session.refresh(role_obj)

        return schemas.Role.from_orm(role_obj)

    @classmethod
    def get_by_name(cls, name: str) -> Optional[Role]:
        return db_session.query(cls.MODEL).filter_by(name=name).first()

    @classmethod
    def get_by_id(cls, id_: str) -> Optional[Role]:
        return db_session.query(cls.MODEL).filter_by(id=id_).first()

    @classmethod
    def get_all(cls) -> list[Role]:
        return db_session.query(cls.MODEL).all()

    @classmethod
    def update_role(cls, role: Role, name: Optional[str], actions: Optional[list[Action]]) -> Role:
        if name:
            role.name = name
        if actions:
            role.actions = actions
        db_session.commit()
        db_session.refresh(role)
        return role

    @classmethod
    def delete_role(cls, role: Role) -> Role:
        db_session.delete(role)
        db_session.commit()
        return role
