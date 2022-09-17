from pydantic import BaseModel, HttpUrl


class Kanji(BaseModel):
    id: str
    literal: str
    meanings: list[str] | None
    onyomi: list[str] | None
    kunyomi: list[str] | None


class Links(BaseModel):
    self: HttpUrl


class Response(BaseModel):
    data: Kanji | None
    links: Links | None
