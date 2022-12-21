from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.sql import func
from db import database


class ShortUrl(database.Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(Text)
    short_url = Column(Text)
    date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=func.now())
