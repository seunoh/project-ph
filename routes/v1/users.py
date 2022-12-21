from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from core.dependencies import get_db, get_current_user
from core.jwt_helper import create_token, validate_token
from crud import crud_user
from models.user import User
from schemas import schema_user

router = APIRouter()


@router.post('/register')
def register(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    """
    고객은 "email" 과 "password" 통해서 회원가입을 할 수 있습니다.
    :param user: {"email":string", "password": string"}
    :param db: database connection
    :return: {"id": int, "email": string}
    """
    db_user = crud_user.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="해당 이메일은 이미 존재 합니다.")
    db_user = crud_user.create_user(db=db, user=user)
    if db_user:
        return {"id": db_user.id, 'email': db_user.email}
    else:
        raise HTTPException(status_code=400, detail="해당 이메일은 이미 존재 합니다.")


@router.post('/login')
def login(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    """
    고객은 "email" 과 "password" 통해서 로그인을 할 수 있으며, "access_token" 값을 확인 할 수 있습니다.
    :param user: {"email":string", "password": string"}
    :param db: database connection
    :return: {"access_token": token}
    """
    db_user = crud_user.get_user_by_email(db=db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못 입력 되었습니다.")

    if bcrypt.verify(user.password, db_user.hashed_password):
        new_token = create_token(email=db_user.email, is_refresh=False)
        refresh_token = create_token(email=db_user.email, is_refresh=True)
        db_token = crud_user.create_token(db=db, token=new_token, refresh_token=refresh_token, user_id=db_user.id)
        if db_token:
            return {'access_token': new_token, 'refresh_token': refresh_token}
        else:
            raise HTTPException(status_code=500, detail="알수 없는 에러가 발생 하였습니다.")
    else:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못 입력 되었습니다.")


@router.post('/logout')
def logout(db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)):
    """
    현재 로그인 된 고객은 로그아웃 할 수 있습니다.
    :param db: database connection
    :param current_user: 현재 로그인 된 사용자
    :return:
    """
    if crud_user.delete_token(db=db, user_id=current_user.id):
        return 'ok'
    else:
        raise HTTPException(status_code=401, detail="로그인이 필요한 기능입니다.")


@router.post('/refresh')
def refresh(refresh_token: str,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):
    """
    "refresh_token" 을 이용하여, 새로운 인증을 받을 수 있습니다.
    :param refresh_token:
    :param db: database connection
    :param current_user: 현재 로그인 된 사용자
    :return:
    """

    token = crud_user.get_token_by_refresh(db=db, refresh_token=refresh_token, user_id=current_user.id)
    if validate_token(refresh_token) and token:
        new_token = create_token(email=current_user.email, is_refresh=False)
        refresh_token = create_token(email=current_user.email, is_refresh=True)
        db_token = crud_user.create_token(db=db, token=new_token, refresh_token=refresh_token, user_id=current_user.id)
        if db_token:
            return {'access_token': new_token, 'refresh_token': refresh_token}
    else:
        raise HTTPException(status_code=401, detail="로그인이 필요한 기능입니다.")
