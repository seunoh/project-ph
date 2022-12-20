from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from crud import crud_user
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db)
):
    """
    // TODO("user_id")
    :param db:
    :return:
    """
    user = crud_user.get(db, user_id=1)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
