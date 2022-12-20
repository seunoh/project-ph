from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from models.user import User
from schemas import schema_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by(db: Session, email: str, password: str):
    db_user = get_user_by_email(db, email)
    if not db_user:
        return None

    if bcrypt.verify(password, db_user.hashed_password):
        return db_user


def create_user(db: Session, user: schema_user.UserCreate):
    hashed_password = bcrypt.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
