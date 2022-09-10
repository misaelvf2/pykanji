from bs4 import BeautifulSoup
from sqlalchemy import create_engine, select
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


if __name__ == "__main__":
    engine = create_engine("sqlite+pysqlite:///kanji.db", echo=False, future=True)

    with Session(engine) as session:
        stmt = select(Reading).where(Reading.reading.in_(["コウ"]))

        count = 0
        for res in session.scalars(stmt):
            print(res.kanji[0].literal)
            count += 1
        print(f"{count} Kanji")
