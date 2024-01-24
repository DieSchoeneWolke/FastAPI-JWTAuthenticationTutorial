from fastapi import FastAPI, Depends
from sqlmodel import Session
from . import database, models_and_schemas, crud

app = FastAPI()

@app.on_event("startup")
def startup_event():
    database.create_db_and_tables()

@app.on_event("shutdown")
def shutdown_event():
    database.shutdown()


@app.post("/register")
def register_user(user: models_and_schemas.UserSchema, db: Session = Depends(database.get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user