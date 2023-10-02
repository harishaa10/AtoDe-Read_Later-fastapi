from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class LinkDB(Base):

    __tablename__ = "links"

    link_id = Column(Integer, primary_key=True, index=True)
    link_url = Column(String, nullable=False)
    category = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    user = relationship("UserDB")

class UserDB(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default= text('now()'))
