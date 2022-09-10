from bs4 import BeautifulSoup
from sqlalchemy import create_engine, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from KanjiDicReader import KanjiDicReader
from models import Kanji, Reading


def store_kanji():
    with Session(engine) as session:
        with open("kanjidic2.xml") as fp:
            soup = BeautifulSoup(fp, "xml")

            my_reader = KanjiDicReader(soup=soup)

            for kanji in my_reader.make_all_kanji():
                session.add(kanji)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


def most_common_readings(n):
    stmt = (
        select(Reading.reading, func.count(Reading.reading).label("count"))
        .where(Reading.category == "onyomi")
        .order_by(func.count(Reading.reading).desc())
        .group_by(Reading.reading)
        .limit(n)
    )
    return stmt


if __name__ == "__main__":
    engine = create_engine("sqlite+pysqlite:///kanji.db", echo=False, future=True)

    with Session(engine) as session:
        result = session.execute(most_common_readings(5))
        print(result.all())
