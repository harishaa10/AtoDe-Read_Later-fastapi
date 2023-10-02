from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def get_access_token(data: dict):
    data_copy = data.copy()
    expire_at= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy.update({"exp": expire_at})
    token= jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify(token: str, credentials_exception):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        return id
    except JWTError:
        raise credentials_exception
    
def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify(token, credentials_exception)
    user = db.query(models.UserDB).filter(models.UserDB.user_id == user_id).first()
    user= schemas.ResponseUser.from_orm(user)
    return user
    


