import typing

from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class AccountBookCreate(BaseModel):
    amount: float
    description: str


class AccountBookUpdate(BaseModel):
    amount: float
    description: typing.Union[str, None] = None


class TokenCreate(BaseModel):
    refresh_token: str


class ShortUrlCreate(BaseModel):
    url: str
