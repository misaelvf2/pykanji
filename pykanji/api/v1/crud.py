from pykanji import models
from sqlalchemy import or_
from sqlalchemy.orm import Session


def read_kanji(db: Session, literal: str):
    return db.query(models.Kanji).filter(models.Kanji.literal == literal).first()


# TODO: Figure out if there is a better way to do this.
def read_all_kanji(
    db: Session,
    reading: list[str] | None = None,
    meaning: list[str] | None = None,
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
        )
        query = query.filter(models.Reading.reading.in_(reading))
    if meaning is not None:
        exps = [models.Meaning.meaning.ilike(f"%{m}") for m in meaning]
        query = query.filter(or_(*exps))
    query = query.limit(limit).all()
    return query
