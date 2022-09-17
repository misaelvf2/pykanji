from pykanji import models
from sqlalchemy.orm import Session


def read_kanji(db: Session, literal: str):
    return db.query(models.Kanji).filter(models.Kanji.literal == literal).first()
