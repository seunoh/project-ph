from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, \
    Text, func

from app.db import database


class AccountBook(database.Base):
    __tablename__ = "account_books"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, default=0.0)
    description = Column(Text, nullable=True)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    created_at = Column(DateTime(timezone=True), default=func.now())
