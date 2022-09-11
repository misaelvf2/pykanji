from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from KanjiDicReader import KanjiDicReader


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
    store_kanji()
