from passlib.context import CryptContext
from . import models_and_schemas
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

JWT_SECRET = "dubasbduea#"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: models_and_schemas.User):
    claims = {
        "sub": user.username,
        "email": user.email,
        "role": user.role,
        "active": user.is_active,
        "exp": datetime.utcnow() + timedelta(minutes=120)
    }

    return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=ALGORITHM)

def decode_token(token):
    claims = jwt.decode(token, key=JWT_SECRET)
    return claims

def check_active(token: str = Depends(oauth2_scheme)):
    claims = decode_token(token)
    if claims.get("active"):
        return claims
    raise HTTPException(
        status_code=401,
        detail="Please activate your account",
        headers={"WWW-Authenticate": "Bearer"}
    )

def check_admin(claims: dict = Depends(check_active)):
    role = claims.get("role")
    if role != "admin":
        raise HTTPException(
        status_code=403,
        detail="Not allowed",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return claims