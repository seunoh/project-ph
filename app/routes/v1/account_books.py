from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.crud import crud_account_book
from app.models.user import User
from app.schemas import AccountBookCreate, AccountBookUpdate

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
        payload: AccountBookCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> Any:
    """
    가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.create_account_book(
        db=db, data=payload, user_id=current_user.id
    )
    if db_obj:
        return {
            "id": db_obj.id,
            "amount": db_obj.amount,
            "description": db_obj.description,
            "date": db_obj.date,
            "updated_at": db_obj.updated_at,
            "created_at": db_obj.created_at,
        }
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="알수 없는 에러가 발생 하였습니다."
    )


@router.put("/{item_id}")
async def update(
        item_id: int,
        payload: AccountBookUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> Any:
    """
    가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.update(
        db=db, data_id=item_id, target=payload, user_id=current_user.id
    )
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="해당 내역을 찾을 수 없습니다."
        )
    return {
        "id": db_obj.id,
        "amount": db_obj.amount,
        "description": db_obj.description,
        "date": db_obj.date,
        "updated_at": db_obj.updated_at,
        "created_at": db_obj.created_at,
    }


@router.delete("/{item_id}")
async def delete(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> Any:
    """
    가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.delete(db=db,
                                      data_id=item_id,
                                      user_id=current_user.id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="해당 내역을 찾을 수 없습니다."
        )
    return {"message": "success"}


@router.get("/")
async def read_all(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다.
    :return:
    """
    db_objs = crud_account_book.get_list_by_user(db=db,
                                                 user_id=current_user.id)
    if not db_objs:
        return []
    return [
        {
            "id": i.id,
            "amount": i.amount,
            "description": i.description,
            "date": i.date,
            "updated_at": i.updated_at,
            "created_at": i.created_at,
        }
        for i in db_objs
        if i
    ]


@router.get("/{item_id}")
async def read(item_id: int, db: Session = Depends(get_db)) -> Any:
    """
    가계부에서 상세한 세부 내역을 볼 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.get(db=db, data_id=item_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="해당 내역을 찾을 수 없습니다."
        )
    return {
        "id": db_obj.id,
        "amount": db_obj.amount,
        "description": db_obj.description,
        "date": db_obj.date,
        "updated_at": db_obj.updated_at,
        "created_at": db_obj.created_at,
    }


@router.post("/{item_id}/copy", status_code=status.HTTP_201_CREATED)
async def copy(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> Any:
    """
    가계부의 세부 내역을 복제할 수 있습니다.
    :return:
    """
    db_obj = crud_account_book.copy(db=db,
                                    data_id=item_id,
                                    user_id=current_user.id)
    if db_obj:
        return {
            "id": db_obj.id,
            "amount": db_obj.amount,
            "description": db_obj.description,
            "date": db_obj.date,
            "updated_at": db_obj.updated_at,
            "created_at": db_obj.created_at,
        }
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="알수 없는 에러가 발생 하였습니다."
    )
