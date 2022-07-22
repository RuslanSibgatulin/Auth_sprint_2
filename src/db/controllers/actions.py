from typing import Optional

import models.actions as schemas
from db import models as models
from db.base import db_session
from db.models import Action


class ActionController:
    MODEL = models.Action

    @classmethod
    def create(cls, action: schemas.ActionCreate) -> schemas.Action:
        new_obj = cls.MODEL(name=action.name)
        db_session.add(new_obj)
        db_session.commit()
        db_session.refresh(new_obj)
        return schemas.Action.from_orm(new_obj)

    @classmethod
    def get_by_name(cls, name: str) -> Optional[Action]:
        return db_session.query(cls.MODEL).filter_by(name=name).first()

    @classmethod
    def get_by_names(cls, names: list[str]) -> list[Action]:
        return db_session.query(cls.MODEL).filter(cls.MODEL.name.in_(names)).all()

    @classmethod
    def get_by_id(cls, id_: str) -> Optional[Action]:
        return db_session.query(cls.MODEL).filter_by(id=id_).first()

    @classmethod
    def get_all(cls) -> list[Action]:
        return db_session.query(cls.MODEL).all()

    @classmethod
    def delete_role(cls, action: Action) -> Action:
        db_session.delete(action)
        db_session.commit()
        return action
