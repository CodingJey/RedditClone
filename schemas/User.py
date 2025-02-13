from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True,autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    nickname = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    date_of_birth = Column(Date)
    date_of_creation = Column(Date)
    posts = relationship("Post", back_populates="poster", cascade="all, delete, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete, delete-orphan")
