from typing import Optional

import bcrypt
from sqlalchemy.orm import Session

from app.models.user import Token, User
from app.schemas import UserCreate


def get_user_by_email(db: Session, email: Optional[str]) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> Optional[User]:
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_token(
    db: Session, token: str, refresh_token: str, user_id: int
) -> Optional[Token]:
    db_obj = Token(token=token, refresh_token=refresh_token, user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_token(db: Session,
              token: Optional[str],
              user_id: int) -> Optional[Token]:
    obj = (
        db.query(Token)
        .filter(Token.token == token and Token.user_id == user_id)
        .first()
    )
    return obj


def get_token_by_refresh(
    db: Session, refresh_token: str, user_id: int
) -> Optional[Token]:
    obj = (
        db.query(Token)
        .filter(Token.refresh_token == refresh_token
                and Token.user_id == user_id)
        .first()
    )
    return obj


def delete_token(db: Session, token: str, user_id: int) -> Optional[Token]:
    obj = (
        db.query(Token)
        .filter(Token.token == token and Token.user_id == user_id)
        .first()
    )
    if obj:
        db.delete(obj)
        db.commit()
        return obj
    return None


def update_token(db: Session,
                 refresh_token: str,
                 user_id: int) -> Optional[Token]:
    obj = (
        db.query(Token)
        .filter(Token.refresh_token == refresh_token
                and Token.user_id == user_id)
        .first()
    )
    if obj:
        db.delete(obj)
        db.commit()
        return obj
    return None
