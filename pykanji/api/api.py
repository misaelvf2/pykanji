import pprint

import pykanji.models as models
from fastapi import Depends, FastAPI, HTTPException
from pykanji.api import crud, schemas
from pykanji.database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/kanji/{literal}", response_model=schemas.Kanji)
def read_kanji(literal: str, db: Session = Depends(get_db)):
    db_kanji = crud.get_kanji(db, literal=literal)
    if db_kanji is None:
        raise HTTPException(status_code=404, detail="Kanji not found")
    obj = {
        "id": db_kanji.id,
        "literal": db_kanji.literal,
        "meanings": [meaning.meaning for meaning in db_kanji.meanings],
        "onyomi": [
            reading.reading
            for reading in db_kanji.readings
            if reading.category == "onyomi"
        ],
        "kunyomi": [
            reading.reading
            for reading in db_kanji.readings
            if reading.category == "kunyomi"
        ],
    }
    return obj
