from pydantic import BaseModel


class MeaningBase(BaseModel):
    meaning: str

    class Config:
        orm_mode = True


class KanjiBase(BaseModel):
    literal: str

    class Config:
        orm_mode = True


class ReadingBase(BaseModel):
    # TODO: Make this into an enum.
    category: str
    reading: str

    class Config:
        orm_mode = True


class Meaning(MeaningBase):
    id: int
    kanji_id: int
    kanji: KanjiBase


class Reading(ReadingBase):
    id: int
    kanji: KanjiBase


class Kanji(KanjiBase):
    id: int
    meanings: list[MeaningBase]
    readings: list[ReadingBase]
