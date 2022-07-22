import uuid

from pydantic import BaseModel


class UserRoleBase(BaseModel):
    user_id: uuid.UUID
    role_id: int


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleDelete(UserRoleBase):
    pass


class UserRole(UserRoleBase):
    class Config:
        orm_mode = True
