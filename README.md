# Payhere

---

## Project

- `Python 3.11` 버전을 사용하였습니다.
- `FastAPI` 를 이용하여 프로젝트 구현 하였습니다.
    - `Depends` 를 활용하여, 로그인이 되어 있는지 체크 하였고, 로그인이 되어 있지 않으면, `401` 에러를 전달 합니다.
- `pydantic` 라이브러리를 활용하였습니다.
    - 환경변수는 `.env` 파일에 기록하며, `pydantic`의 `BaseSetting` 을 활용하여, `.env` 파일에 있는 내용을 자동으로 Python 의 변수와 매핑 하여, `config.py` 에서 사용 할수
      있도록 하였습니다.
- `SQLAlchemy` 를 이용 하여, MySQL 연결 하였고, ORM(Object Relational Mapping) 를 활용하였습니다.
- `crud` 에서 데이터베이스와 관련된 로직이 구현 되었습니다.
- `routes` 에서는 API 기능들이 구현 되었고, `v1` 를 추가하여, API 의 versioning 기능을 추가하였습니다.
- `schemas.py` 는 API의 파라미터 모델 클래스들이 구성 되어 있습니다.
- `httpx` 와 `pytest` 를 이용하여 테스트 코드를 추가 하였습니다.

## Requirements

    Python 3.8+ 

## Environment Variables

### `SECRET_KEY`

`JWT` 의 암호화 시 필요한 키

### `DATABASE_URL`

데이터베이스 연결

## 폴더 구조

```
payhere
│   README.md
│   .gitignore
│   requirements.txt    
│
└───app
│   │   main.py
│   │   schemas.py
│   └───core
│       │   config.py
│       │   dependencies.py
│       │   jwt_helper.py
│   └───curd
│       │   crud_account_book.py
│       │   crud_short_url.py
│       │   crud_user.py
│   └───db
│       │   database.py
│       │   init_query.py
│   └───models
│       │   account_book.py
│       │   short_url.py
│       │   user.py
│   └───routes
│       │   short_url.py
│       └───v1
│           │   account_books.py
│           │   users.py
│   
└───tests
    │   test_*.py : 테스트 파일
 
```

## 기능

- [x] 고객은 이메일과 비밀번호 입력을 통해서 회원 가입을 할 수 있습니다.
- [x] 고객은 회원 가입이후, 로그인과 로그아웃을 할 수 있습니다.
- [x] 고객은 로그인 이후 가계부 관련 아래의 행동을 할 수 있습니다.
- [x] 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
- [x] 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다.
- [x] 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.
- [x] 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다.
- [x] 가계부에서 상세한 세부 내역을 볼 수 있습니다.
- [x] 가계부의 세부 내역을 복제할 수 있습니다.
- [x] 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
- [x] 로그인하지 않은 고객은 가계부 내역에 대한 접근 제한 처리가 되어야 합니다.

### 추가 기능

- [x] `flake8`, `black` 를 이용하여 코드 정리
- [x] `pytest` 를 활용하여 테스트 코드 추가
- [x] api 의 `vX` 버전 추가

### 다음 기능

- [ ] Docker 적용
- [ ] Database Migration 기능
- [ ] 고객의 email 또는 password 찾기 (또는 리셋)
- [ ] 통계자료 만들기

### 참고자료

[FastAPI-ko](https://fastapi.tiangolo.com/ko/)
[Pydantic](https://docs.pydantic.dev/)