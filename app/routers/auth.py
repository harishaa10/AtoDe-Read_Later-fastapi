from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import  utils, models, oauth2, schemas

app = APIRouter(tags= ["Auth"])

@app.post("/login", response_model= schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    #OAuth2PasswordRequestForm is a class that has two attributes: username and password
    
    user= db.query(models.UserDB).filter(models.UserDB.email == user_cred.username).first()
    if user and utils.verify(user_cred.password, user.password):
        access_token= oauth2.get_access_token(data= {"user_id" : user.user_id})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Invalid Credentials")