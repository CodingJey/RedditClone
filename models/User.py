from sqlalchemy import create_engine, Column, Integer, String, Date,DateTime, Boolean
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True,autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    nickname = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    date_of_birth = Column(Date)
    date_of_joining = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean)
    # posts = relationship("Post", back_populates="poster", cascade="all, delete, delete-orphan")
    # subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete, delete-orphan")
