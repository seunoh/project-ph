from sqlalchemy import Column, Integer, DateTime, Text, func

from app.db import database


class ShortUrl(database.Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(Text)
    short_url = Column(Text)
    expire = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=func.now())
