from pydantic import BaseModel


class ActionBase(BaseModel):
    name: str


class ActionCreate(ActionBase):
    pass


class Action(ActionBase):
    id: int

    class Config:
        orm_mode = True
