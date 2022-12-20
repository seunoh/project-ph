from sqlalchemy import Column, Integer, Text, Float, DateTime, ForeignKey

from db import database


class AccountBook(database.Base):
    __tablename__ = 'account_books'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, default=0.0)
    description = Column(Text, nullable=True)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
