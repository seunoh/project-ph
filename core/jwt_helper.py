from datetime import datetime, timezone, timedelta

import jwt

from core.config import settings


def validate_token(token):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    except jwt.ExpiredSignatureError as e:
        raise e
    except jwt.InvalidTokenError as e:
        raise e


def create_token(email, is_refresh: bool):
    exp = datetime.utcnow() + timedelta(hours=3)
    if is_refresh:
        exp = datetime.utcnow() + timedelta(days=1)

    return jwt.encode({'email': email, "exp": exp}, settings.SECRET_KEY, algorithm='HS256')
