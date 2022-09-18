import pykanji.models as models
from fastapi import Depends, FastAPI, HTTPException, Query
from pykanji.api.v1 import crud, schemas
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


@app.get(
    "/api/v1/kanji/{literal}",
    response_model=schemas.Response,
    response_model_exclude_unset=True,
)
def read_kanji(literal: str, db: Session = Depends(get_db)):
    db_kanji = crud.read_kanji(db, literal=literal)
    if db_kanji is None:
        raise HTTPException(status_code=404, detail="Kanji not found")
    res = {
        "data": {
            "id": str(db_kanji.id),
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
        },
        "links": {"self": f"http://127.0.0.1:8000/api/v1/kanji/{literal}"},
    }
    return res


@app.get(
    "/api/v1/kanji", response_model=schemas.Response, response_model_exclude_unset=True
)
# TODO: Look into implementing more advanced filtering logic
# with a dedicated "filter" query parameter
# Query parameters are currently interpreted as follows:
# (M1 | M2 | ... | Mn) && (R1 | R2 | ... | Rm),
# Where M = Meaning, R = reading
# This logic is implemented in the crud.py DB call
def read_all_kanji(
    reading: list[str] | None = Query(default=None),
    meaning: list[str] | None = Query(default=None),
    limit: int = 10,
    db: Session = Depends(get_db),
):
    db_kanji = crud.read_all_kanji(db, reading=reading, meaning=meaning, limit=limit)
    if db_kanji is None:
        raise HTTPException(status_code=404, detail="No Kanji found matching criteria")
    res = {
        "data": [
            {
                "id": str(kanji.id),
                "literal": kanji.literal,
                "meanings": [meaning.meaning for meaning in kanji.meanings],
                "onyomi": [
                    reading.reading
                    for reading in kanji.readings
                    if reading.category == "onyomi"
                ],
                "kunyomi": [
                    reading.reading
                    for reading in kanji.readings
                    if reading.category == "kunyomi"
                ],
            }
            for kanji in db_kanji
        ]
    }
    return res
