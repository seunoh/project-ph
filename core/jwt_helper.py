import jwt

from core.config import settings


def validate_token(token):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    except jwt.ExpiredSignatureError as e:
        raise e
    except jwt.InvalidTokenError as e:
        raise e


def encode_token(email):
    return jwt.encode({'id': email}, settings.SECRET_KEY, algorithm='HS256')
