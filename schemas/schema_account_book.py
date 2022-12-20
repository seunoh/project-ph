import typing

from pydantic import BaseModel


class AccountBookBase(BaseModel):
    amount: float


class AccountBookCreate(AccountBookBase):
    description: str


class AccountBookUpdate(AccountBookBase):
    description: typing.Union[str, None] = None


class User(AccountBookBase):
    id: int
    date: str

    class Config:
        orm_mode = True
