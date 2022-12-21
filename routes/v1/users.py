from fastapi import APIRouter, Depends, HTTPException, status
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from core.dependencies import get_db, get_current_user, get_current_token
from core.jwt_helper import create_token, validate_token
from crud import crud_user
from models.user import User
from schemas import TokenCreate
from schemas import UserCreate

router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    고객은 "email" 과 "password" 통해서 회원가입을 할 수 있습니다.
    :param payload: {"email":string", "password": string"}
    :param db: database connection
    :return: data: {"id": int, "email": string}, status_code: 201, 400
    """
    db_user = crud_user.get_user_by_email(db=db, email=payload.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 이메일은 이미 존재 합니다.")
    db_user = crud_user.create_user(db=db, user=payload)
    if db_user:
        return {"id": db_user.id, 'email': db_user.email}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 이메일은 이미 존재 합니다.")


@router.post('/login')
def login(payload: UserCreate, db: Session = Depends(get_db)):
    """
    고객은 "email" 과 "password" 통해서 로그인을 할 수 있으며, "access_token" 값을 확인 할 수 있습니다.
    :param payload: {"email":string", "password": string"}
    :param db: database connection
    :return: {"access_token": token}
    """
    db_user = crud_user.get_user_by_email(db=db, email=payload.email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호가 잘못 입력 되었습니다.")

    if bcrypt.verify(payload.password, db_user.hashed_password):
        new_token = create_token(email=db_user.email, is_refresh=False)
        refresh_token = create_token(email=db_user.email, is_refresh=True)
        db_token = crud_user.create_token(db=db, token=new_token, refresh_token=refresh_token, user_id=db_user.id)
        if db_token:
            return {'access_token': new_token, 'refresh_token': refresh_token}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="알수 없는 에러가 발생 하였습니다.")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호가 잘못 입력 되었습니다.")


@router.post('/logout')
def logout(db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user),
           current_token: str = Depends(get_current_token)):
    """
    현재 로그인 된 고객은 로그아웃 할 수 있습니다.
    :param db: database connection
    :param current_user: 현재 로그인 된 사용자
    :param current_token: "authorization" in header
    :return:
    """
    if crud_user.delete_token(db=db, token=current_token, user_id=current_user.id):
        return {'message': 'OK'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인이 필요한 기능입니다.")


@router.post('/refresh')
async def refresh(payload: TokenCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    """
    "refresh_token" 을 이용하여, 새로운 인증을 받을 수 있습니다.
    :param payload:
    :param db: database connection
    :param current_user: 현재 로그인 된 사용자
    :return:
    """

    try:
        refresh_token = payload.refresh_token

        db_token = crud_user.get_token_by_refresh(db=db, refresh_token=refresh_token, user_id=current_user.id)
        if validate_token(refresh_token) and db_token:
            new_token = create_token(email=current_user.email, is_refresh=False)
            refresh_token = create_token(email=current_user.email, is_refresh=True)
            new_db_token = crud_user.create_token(db=db, token=new_token, refresh_token=refresh_token,
                                                  user_id=current_user.id)
            if new_db_token:
                return {'access_token': new_token, 'refresh_token': refresh_token}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인이 필요한 기능입니다.")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="'refresh_token' 키 값이 존재 하지 않습니다. ")
