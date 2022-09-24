from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError

import models
from database import SessionLocal, engine
from KanjiDicReader import KanjiDicReader

KANJIDIC_PATH = "kanjidic2.xml"


def create_tables():
    models.Base.metadata.create_all(engine)


# TODO: Refactor so Session is passed via dependency injection
def store_kanji(limit: int = None):
    with SessionLocal() as session:
        with open(KANJIDIC_PATH) as fp:
            soup = BeautifulSoup(fp, "xml")

            my_reader = KanjiDicReader(soup=soup, limit=limit)

            for kanji in my_reader.make_all_kanji():
                session.add(kanji)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


if __name__ == "__main__":
    create_tables()
    store_kanji()
