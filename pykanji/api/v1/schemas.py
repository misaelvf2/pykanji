from pydantic import BaseModel, HttpUrl


class Kanji(BaseModel):
    id: str
    literal: str
    meanings: list[str] | None
    grade: int | None
    stroke_count: int | None
    jlpt: int | None
    frequency: int | None
    onyomi: list[str] | None
    kunyomi: list[str] | None
    nanori: list[str] | None


class Links(BaseModel):
    self: HttpUrl


class Response(BaseModel):
    data: Kanji | list[Kanji] | None
    links: Links | None
