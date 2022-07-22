from pydantic import BaseModel

from models.actions import Action


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    actions: list[str]


class Role(RoleBase):
    id: int
    actions: list[Action]

    class Config:
        orm_mode = True
