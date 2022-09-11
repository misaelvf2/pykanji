from pykanji import models
from sqlalchemy.orm import Session


def get_kanji(db: Session, literal: str):
    return db.query(models.Kanji).filter(models.Kanji.literal == literal).first()
