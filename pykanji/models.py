from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from pykanji.database import Base

kanji_reading = Table(
    "kanji_reading",
    Base.metadata,
    Column("kanji_id", Integer, ForeignKey("kanji.id"), primary_key=True),
    Column("reading_id", Integer, ForeignKey("reading.id"), primary_key=True),
)

kanji_nanori = Table(
    "kanji_nanori",
    Base.metadata,
    Column("kanji_id", Integer, ForeignKey("kanji.id"), primary_key=True),
    Column("nanori_id", Integer, ForeignKey("nanori.id"), primary_key=True),
)


class Kanji(Base):
    __tablename__ = "kanji"

    id = Column(Integer, primary_key=True)
    literal = Column(String, unique=True)
    grade = Column(Integer)
    stroke_count = Column(Integer)
    jlpt = Column(Integer)
    frequency = Column(Integer)
    meanings = relationship("Meaning", back_populates="kanji")
    readings = relationship("Reading", secondary=kanji_reading, back_populates="kanji")
    nanori = relationship("Nanori", secondary=kanji_nanori, back_populates="kanji")

    def __repr__(self):
        return (
            f"Kanji(id={self.id!r}, literal={self.literal!r}, grade={self.grade!r}, stroke_count={self.stroke_count!r} "
            f"jlpt={self.jlpt!r}, frequency={self.frequency!r}, "
            f"meanings={self.meanings!r}, readings={self.readings!r}), "
            f"nanori={self.nanori!r}"
        )


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


class Nanori(Base):
    __tablename__ = "nanori"

    id = Column(Integer, primary_key=True)
    nanori = Column(String)
    kanji = relationship("Kanji", secondary=kanji_nanori, back_populates="nanori")

    def __repr__(self):
        return f"Nanori(id={self.id!r}, nanori={self.nanori!r})"
