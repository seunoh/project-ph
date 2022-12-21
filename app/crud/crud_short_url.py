import nanoid
from sqlalchemy.orm import Session

from app.models.short_url import ShortUrl


def get_by_url(db: Session, short_url: str):
    return db.query(ShortUrl).filter(ShortUrl.short_url == short_url).first()


def create_short_url(db: Session, original_url: str, base_url: str):
    nano_id = nanoid.generate(size=10)
    db_obj = db.query(ShortUrl).filter(ShortUrl.original_url == original_url).first()
    if not db_obj:
        short_url = f"{base_url}{nano_id}"
        db_obj = ShortUrl(original_url=original_url, short_url=short_url)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    return db_obj
