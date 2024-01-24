from sqlmodel import Session
from . import models_and_schemas

def create_user(db: Session, user: models_and_schemas.UserSchema):
    hashed_password = user.password + "hashed"
    db_user = models_and_schemas.User(
        email=user.email,
        username=user.username,
        role=user.role,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh()
    return db_user