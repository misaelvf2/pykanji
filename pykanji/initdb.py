from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError

import models
from database import SessionLocal, engine
from KanjiDicReader import KanjiDicReader

KANJIDIC_PATH = "kanjidic2.xml"

models.Base.metadata.create_all(bind=engine)


def create_tables():
    models.Base.metadata.create_all(engine)


def store_kanji():
    with SessionLocal() as session:
        with open(KANJIDIC_PATH) as fp:
            soup = BeautifulSoup(fp, "xml")

            my_reader = KanjiDicReader(soup=soup)

            for kanji in my_reader.make_all_kanji():
                session.add(kanji)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


if __name__ == "__main__":
    create_tables()
    store_kanji()
