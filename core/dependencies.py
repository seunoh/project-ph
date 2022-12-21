import jwt
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from core.jwt_helper import validate_token
from crud import crud_user
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
):
    """
    :param request:
    :param db:
    :return:
    """
    authorization = request.headers.get('authorization')
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='로그인이 필요한 기능입니다.')

    token = authorization.split(' ')[1]
    try:
        payload = validate_token(token)
        user = crud_user.get_user_by_email(db, email=payload.get_by_url('id'))
        db_token = crud_user.get_token(db, token, user_id=user.id)
        if not user or not db_token:
            raise HTTPException(status_code=401, detail='로그인이 필요한 기능입니다.')
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail='로그인이 필요한 기능입니다.')
