from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base

kanji_reading = Table(
    "kanji_reading",
    Base.metadata,
    Column("kanji_id", Integer, ForeignKey("kanji.id"), primary_key=True),
    Column("reading_id", Integer, ForeignKey("reading.id"), primary_key=True),
)


# TODO Add misc columns
class Kanji(Base):
    __tablename__ = "kanji"

    id = Column(Integer, primary_key=True)
    literal = Column(String, unique=True)
    meanings = relationship("Meaning", back_populates="kanji")
    # TODO Split readings column into kun- and on- columns
    readings = relationship("Reading", secondary=kanji_reading, back_populates="kanji")

    def __repr__(self):
        return f"Kanji(id={self.id!r}, literal={self.literal!r}, meanings={self.meanings!r}, readings={self.readings!r})"


class Meaning(Base):
    __tablename__ = "meaning"

    id = Column(Integer, primary_key=True)
    meaning = Column(String)
    kanji_id = Column(Integer, ForeignKey("kanji.id"))
    kanji = relationship("Kanji", back_populates="meanings")

    def __repr__(self):
        return f"Meaning(id={self.id!r}, meaning={self.meaning!r})"


class Reading(Base):
    __tablename__ = "reading"

    id = Column(Integer, primary_key=True)
    category = Column(String)
    reading = Column(String)
    kanji = relationship("Kanji", secondary=kanji_reading, back_populates="readings")

    def __repr__(self):
        return f"Reading(id={self.id!r}, category={self.category!r}, reading={self.reading!r})"
