import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from core.dependencies import get_db
from crud import crud
from schemas import schemas

router = APIRouter()


@router.post('/register')
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="해당 이메일은 이미 존재 합니다.")
    return crud.create_user(db=db, user=user)


@router.post('/login')
async def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못 입력 되었습니다.")
    token = jwt.encode({'id': db_user.email}, settings.SECRET_KEY, algorithm='HS256')
    return {'access_token': token}


@router.post('/logout')
async def logout():
    return ''
