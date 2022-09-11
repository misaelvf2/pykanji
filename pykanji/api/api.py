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
    return db_kanji
