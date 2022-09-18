from pykanji import models
from sqlalchemy.orm import Session


def read_kanji(db: Session, literal: str):
    return db.query(models.Kanji).filter(models.Kanji.literal == literal).first()


# TODO: Figure out if there is a better way to do this.
def read_all_kanji(
    db: Session,
    reading: str | None = None,
    meaning: str | None = None,
    limit: int = 10,
):
    query = db.query(models.Kanji)
    if reading is not None:
        query = query.join(models.kanji_reading).join(models.Reading)
    if meaning is not None:
        query = query.join(models.Meaning)
    if reading is not None:
        query = query.filter(
            models.Kanji.id == models.kanji_reading.c.kanji_id,
            models.Reading.reading == reading,
        )
    if meaning is not None:
        query = query.filter(models.Meaning.meaning.ilike(f"%{meaning}%"))
    query = query.limit(limit).all()
    return query
