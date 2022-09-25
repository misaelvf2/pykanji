from sqlalchemy import or_
from sqlalchemy.orm import Session

from pykanji.models import Kanji, Meaning, Reading, kanji_reading


def read_kanji(db: Session, literal: str):
    return db.query(Kanji).filter(Kanji.literal == literal).first()


def read_multiple_kanji(db: Session, literals: list[str]):
    query = db.query(Kanji).filter(Kanji.literal.in_(literals))
    return query


# TODO: Figure out if there is a better way to do this.
def read_all_kanji(
    db: Session,
    literal: list[str] | None = None,
    reading: list[str] | None = None,
    meaning: list[str] | None = None,
    limit: int = 10,
):
    query = db.query(Kanji)
    if reading is not None:
        query = query.join(kanji_reading).join(Reading)
    if meaning is not None:
        query = query.join(Meaning)
    if reading is not None:
        query = query.filter(
            Kanji.id == kanji_reading.c.kanji_id,
        )
        query = query.filter(Reading.reading.in_(reading))
    if meaning is not None:
        exps = [Meaning.meaning.ilike(f"%{m}") for m in meaning]
        query = query.filter(or_(*exps))
    query = query.limit(limit).all()
    return query


def read_most_frequent_kanji(db: Session, n: int, descending=False):
    query = (
        db.query(Kanji)
        .filter(Kanji.frequency != None)
        .order_by(Kanji.frequency.desc() if descending else Kanji.frequency)
        .limit(n)
        .all()
    )
    return query
