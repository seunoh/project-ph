import datetime

from sqlalchemy.orm import Session

from models.account import AccountBook
from schemas import schema_account_book


def get(db: Session, data_id: int, user_id: int):
    return db.query(AccountBook).filter(AccountBook.id == data_id and AccountBook.user_id == user_id).first()


def get_list_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(AccountBook).filter(AccountBook.user_id == user_id).offset(skip).limit(limit).all()


def update(db: Session, data_id: int, target: schema_account_book.AccountBookUpdate, user_id: int):
    obj_data = db.query(AccountBook).filter(AccountBook.id == data_id and AccountBook.user_id == user_id).first()
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


def delete(db: Session, data_id: int, user_id: int):
    obj = db.query(AccountBook).filter(AccountBook.id == data_id and AccountBook.user_id == user_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return obj


def copy(db: Session, data_id: int, user_id):
    obj = db.query(AccountBook).filter(AccountBook.id == data_id and AccountBook.user_id == user_id).first()
    if not obj:
        return None
    db_obj = AccountBook(amount=obj.amount,
                         description=obj.description,
                         date=obj.date,
                         user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_with_user(db: Session, data: schema_account_book.AccountBookCreate, user_id: int):
    date = datetime.datetime.now()
    db_obj = AccountBook(amount=data.amount, description=data.description, date=date, user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
