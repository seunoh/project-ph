from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func

from app.db import database


class User(database.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=func.now())


class Token(database.Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text)
    refresh_token = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
