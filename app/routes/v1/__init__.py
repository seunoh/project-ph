from fastapi import APIRouter

from . import users, account_books

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(account_books.router, prefix="/account-books", tags=["account_books"])
