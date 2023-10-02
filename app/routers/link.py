from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List


app = APIRouter(tags=["Links"])

#Get All links
@app.get("/links", response_model=List[schemas.ResponseLink])
async def get_all_links(db: Session = Depends(get_db), current_user: schemas.ResponseUser =Depends(oauth2.get_user), category: str = None, limit: int = 10, skip: int = 0):
    # cursor.execute("SELECT * FROM links")
    # links=cursor.fetchall()
    if category:
        links= db.query(models.LinkDB).filter(models.LinkDB.user_id== current_user.user_id, models.LinkDB.category== category).limit(limit).offset(skip).all()
    else:
        links = db.query(models.LinkDB).filter(models.LinkDB.user_id== current_user.user_id).limit(limit).offset(skip).all()
    return links

#Get link by id
@app.get("/links/{link_id}", response_model=schemas.ResponseLink)
def get_link_by_id(link_id: int, response: Response, db: Session = Depends(get_db), current_user: schemas.ResponseUser =Depends(oauth2.get_user)):
    # cursor.execute("SELECT * FROM links WHERE link_id = %s", (link_id,))
    # link= cursor.fetchone()
    link= db.query(models.LinkDB).filter(models.LinkDB.link_id == link_id).first()
    if link:
        if link.user_id!= current_user.user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="You are not authorized to view this link")
        return link
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Link not found")

#Add link
@app.post("/links", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseLink)
async def add_link_to_read(link: schemas.Link, db: Session = Depends(get_db), current_user: schemas.ResponseUser =Depends(oauth2.get_user)):
    # cursor.execute("""INSERT INTO links (link_url, category) VALUES (%s, %s) RETURNING *""", (link.link_url, link.category))
    # link = cursor.fetchone()
    #     if link:
    #     conn.commit()
    #     return {"data": link}
    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Link not added")

    link= models.LinkDB(link_url= link.link_url, category= link.category, user_id= current_user.user_id)
    #link= models.LinkDB(**link.dict()) only if the variable names are same
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


#Delete link
@app.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(link_id: int, db: Session = Depends(get_db), current_user: schemas.ResponseUser =Depends(oauth2.get_user)):
    # cursor.execute("DELETE FROM links WHERE link_id = %s RETURNING *", (link_id,))
    # link=cursor.fetchone()
    # if link:
    #     conn.commit()
    #     return {"data": link}
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Link not found")

    link= db.query(models.LinkDB).filter(models.LinkDB.link_id== link_id).first()

    if link== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Link not found")
    
    if link.user_id!= current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="You are not authorized to delete this link")

    
    db.delete(link)
    db.commit()
    return link
    
#Update link
@app.put("/links/{link_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ResponseLink)
async def update_link(link: schemas.Link, link_id: int, db: Session = Depends(get_db), current_user: schemas.ResponseUser =Depends(oauth2.get_user)):
    # cursor.execute("UPDATE links SET link_url = %s, category = %s WHERE link_id = %s RETURNING *", (link.link_url, link.category, link_id))
    # link=cursor.fetchone()
    # if link:
    #     conn.commit()
    #     return {"data": link}
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Link not found")

    to_update_link= db.query(models.LinkDB).filter(models.LinkDB.link_id== link_id)
    if to_update_link.first():
        if to_update_link.first().user_id!= current_user.user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="You are not authorized to update this link")
        to_update_link.update({"link_url": link.link_url, "category": link.category})
        db.commit()
        return to_update_link.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Link not found")
