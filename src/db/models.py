import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        PrimaryKeyConstraint, String, Table, Text,
                        UniqueConstraint, or_)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship

from db.base import Base

role_action = Table(
    "role_action",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), primary_key=True),
    Column("action_id", ForeignKey("action.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    roles = relationship("UserRole", back_populates="user")

    @classmethod
    def get_user_by_universal_login(cls, login: Optional[str] = None, email: Optional[str] = None):
        return cls.query.filter(or_(cls.login == login, cls.email == email)).first()


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    users = relationship("UserRole", back_populates="role")
    actions = relationship("Action", secondary=role_action, backref="roles")


class UserRole(Base):
    __tablename__ = "user_role"

    user_id = Column(ForeignKey("user.id"), primary_key=True)
    role_id = Column(ForeignKey("role.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class LoginHistory(Base):
    __tablename__ = "login_history"
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'login_at'),
    )

    # id = Column(Integer, primary_key=True, unique=True)
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"))
    platform = Column(String(100))
    login_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip = Column(String(100))


class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)


class SocialAccount(Base):
    __tablename__ = "social_account"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship(User, backref=backref("social_accounts", lazy=True))
    social_id = Column(Text, nullable=False)
    social_name = Column(Text, nullable=False)

    __table_args__ = (UniqueConstraint("social_id", "social_name", name="social_pk"),)

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"
