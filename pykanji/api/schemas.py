from models import Kanji
from pydantic import BaseModel


class MeaningBase(BaseModel):
    meaning: str


class Meaning(MeaningBase):
    id: int
    kanji_id: int
    kanji: Kanji

    class Config:
        orm_mode = True


class ReadingBase(BaseModel):
    # TODO: Make this into an enum.
    category: str
    reading: str


class Reading(ReadingBase):
    id: int
    kanji: Kanji

    class Config:
        orm_mode = True


class KanjiBase(BaseModel):
    literal: str


class Kanji(KanjiBase):
    id: int
    meanings: list[Meaning]
    readings: list[Reading]

    class Config:
        orm_mode = True
