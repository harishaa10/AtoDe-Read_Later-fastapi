from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional


class Link(BaseModel):
    link_url: str
    category: Optional[str] = None

class User(BaseModel):
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    email: EmailStr
    user_id: int
    created_at: datetime
    model_config= ConfigDict(from_attributes=True)  

class Token(BaseModel):
    access_token: str
    token_type: str

class ResponseLink(Link):
    link_id: int
    user_id: int
    user: ResponseUser
    model_config= ConfigDict(from_attributes=True)  #Instead of from_orm=True (This is the new version)
