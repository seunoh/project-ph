from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from core.dependencies import get_db
from crud import crud_short_url
from schemas import ShortUrlCreate

router = APIRouter()


@router.post('/short', status_code=status.HTTP_201_CREATED)
async def create(payload: ShortUrlCreate,
                 request: Request,
                 db: Session = Depends(get_db)):
    """
    가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
    (단축 URL은 특정 시간 뒤에 만료되어야 합니다.)
    :return:
    """
    url = payload.url
    base_url = request.base_url

    db_obj = crud_short_url.create_short_url(db=db, original_url=url, base_url=str(base_url))
    return {'original_url': db_obj.original_url, 'short_url': db_obj.short_url}


@router.get('/{short_url}')
async def short(short_url: str,
                request: Request,
                db: Session = Depends(get_db)):
    """
    가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
    (단축 URL은 특정 시간 뒤에 만료되어야 합니다.)
    :return:
    """
    db_obj = crud_short_url.get_by_url(db=db, short_url=f"{request.base_url}{short_url}")
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 데이터를 입력하였습니다.")
    return RedirectResponse(status_code=status.HTTP_301_MOVED_PERMANENTLY, url=db_obj.original_url)
