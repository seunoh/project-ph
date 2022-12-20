from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db, get_current_user
from crud import crud_account_book
from models.user import User
from schemas import schema_account_book

router = APIRouter()


@router.post('/')
async def create(data: schema_account_book.AccountBookCreate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    """
    가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.create_with_user(db, data=data, user_id=current_user.id)
    return db_obj


@router.put('/{item_id}')
async def update(item_id: int,
                 data: schema_account_book.AccountBookUpdate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    """
    가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.update(db, item_id, data, user_id=current_user.id)
    return db_obj


@router.delete('/{item_id}')
async def delete(item_id: int,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    """
    가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.delete(db, item_id, user_id=current_user.id)
    return db_obj


@router.get('/')
async def read_all(db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    """
    가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.get_list_by_user(db, user_id=current_user.id)
    return db_obj


@router.get('/{item_id}')
async def read(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    가계부에서 상세한 세부 내역을 볼 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.get(db, item_id, user_id=current_user.id)
    return db_obj


@router.post('/{item_id}/copy')
async def copy(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    가계부의 세부 내역을 복제할 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.copy(db, item_id, user_id=current_user.id)
    return db_obj


@router.post('/{item_id}/share')
async def share():
    """
    가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
    (단축 URL은 특정 시간 뒤에 만료되어야 합니다.)
    :return:
    """
    return ''
