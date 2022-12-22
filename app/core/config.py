import secrets
from typing import Union

from pydantic import AnyUrl, BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URL: Union[AnyUrl, str] = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
