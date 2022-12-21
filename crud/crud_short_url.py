import nanoid
from sqlalchemy.orm import Session

from models.short_url import ShortUrl


def get(db: Session, url: str):
    return db.query(ShortUrl).filter(ShortUrl.short_url == url).first()


def create_with_user(db: Session, original_url: str, base_url: str):
    nano_id = nanoid.generate()
    db_obj = db.query(ShortUrl).filter(ShortUrl.original_url == original_url).first()
    if not db_obj:
        short_url = f"{base_url}{nano_id}"
        db_obj = ShortUrl(original_url=original_url, short_url=short_url)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    return db_obj
