from fastapi import APIRouter, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

app = APIRouter(prefix="/users", 
                tags=["Users"])

#Create user
@app.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)
def create_user(user:schemas.User, db: Session = Depends(get_db)):

    #hashed password
    user.password = utils.hash(user.password)

    #store in db
    user= models.UserDB(email= user.email, password= user.password)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user 
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="User not created")
    
#get user
@app.get("/{id}", response_model=schemas.ResponseUser)
def get_user(id: int, db: Session = Depends(get_db)):

    user= db.query(models.UserDB).filter(models.UserDB.user_id== id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not found")