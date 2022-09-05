from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

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
    literal = Column(String)
    meanings = relationship("Meaning", back_populates="kanji")
    # TODO Split readings column into kun- and on- columns
    readings = relationship("Reading", secondary=kanji_reading, back_populates="kanji")


class Meaning(Base):
    __tablename__ = "meaning"

    id = Column(Integer, primary_key=True)
    meaning = Column(String)
    kanji_id = Column(Integer, ForeignKey("kanji.id"))
    kanji = relationship("Kanji", back_populates="meanings")


class Reading(Base):
    __tablename__ = "reading"

    id = Column(Integer, primary_key=True)
    category = Column(String)
    reading = Column(String)
    kanji = relationship("Kanji", secondary=kanji_reading, back_populates="readings")
