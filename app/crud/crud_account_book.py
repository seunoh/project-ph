from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.account_book import AccountBook
from app.schemas import AccountBookCreate, AccountBookUpdate


def get(db: Session, data_id: int) -> Optional[AccountBook]:
    return db.query(AccountBook).filter(AccountBook.id == data_id).first()


def get_list_by_user(db: Session, user_id: int) -> Optional[list[AccountBook]]:
    return db.query(AccountBook).filter(AccountBook.user_id == user_id).all()


def update(
        db: Session, data_id: int, target: AccountBookUpdate, user_id: int
) -> Optional[AccountBook]:
    obj_data = (
        db.query(AccountBook)
        .filter(AccountBook.id == data_id and AccountBook.user_id == user_id)
        .first()
    )
    if not obj_data:
        return None
    if target.amount:
        obj_data.amount = target.amount
    if target.description:
        obj_data.description = target.description
    db.add(obj_data)
    db.commit()
    db.refresh(obj_data)
    return obj_data


def delete(db: Session, data_id: int, user_id: int) -> Optional[AccountBook]:
    obj = (
        db.query(AccountBook)
        .filter(AccountBook.id == data_id and AccountBook.user_id == user_id)
        .first()
    )
    if obj:
        db.delete(obj)
        db.commit()
        return obj
    return None


def copy(db: Session, data_id: int, user_id: int) -> Optional[AccountBook]:
    obj = (
        db.query(AccountBook)
        .filter(AccountBook.id == data_id and AccountBook.user_id == user_id)
        .first()
    )
    if not obj:
        return None
    db_obj = AccountBook(
        amount=obj.amount,
        description=obj.description,
        date=obj.date,
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_account_book(
        db: Session,
        data: AccountBookCreate,
        user_id: int
) -> Optional[AccountBook]:
    _date = datetime.strptime(data.date, "%Y-%m-%d").date()
    db_obj = AccountBook(
        amount=data.amount,
        description=data.description,
        date=_date,
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
