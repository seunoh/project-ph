from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from core.dependencies import get_db
from crud import crud_short_url

router = APIRouter()


@router.post('/short')
async def create(url: str, request: Request, db: Session = Depends(get_db)):
    """
    가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
    (단축 URL은 특정 시간 뒤에 만료되어야 합니다.)
    :return:
    """
    base_url = request.base_url

    db_obj = crud_short_url.create_with_user(db, url, str(base_url))
    return db_obj


@router.get('/{short_url}')
async def short(short_url: str, db: Session = Depends(get_db)):
    """
    가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
    (단축 URL은 특정 시간 뒤에 만료되어야 합니다.)
    :return:
    """
    db_obj = crud_short_url.get_by_url(db, short_url)
    if not db_obj:
        raise HTTPException(status_code=404, detail="해당 페이지를 찾을 수 없습니다.")
    return RedirectResponse(url=db_obj.original_url)
