import secrets

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URL: AnyUrl = ''

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False


settings = Settings()
