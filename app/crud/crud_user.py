from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from app.models.user import User, Token
from app.schemas import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_token(db: Session, token: str, refresh_token: str, user_id: int):
    db_obj = Token(token=token, refresh_token=refresh_token, user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_token(db: Session, token: str, user_id: int):
    obj = db.query(Token).filter(Token.token == token and Token.user_id == user_id).first()
    return obj


def get_token_by_refresh(db: Session, refresh_token: str, user_id: int):
    obj = db.query(Token).filter(Token.refresh_token == refresh_token and Token.user_id == user_id).first()
    return obj


def delete_token(db: Session, token: str, user_id: int):
    obj = db.query(Token).filter(Token.token == token and Token.user_id == user_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return obj


def update_token(db: Session, refresh_token: str, user_id: int):
    obj = db.query(Token).filter(Token.refresh_token == refresh_token and Token.user_id == user_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return obj
