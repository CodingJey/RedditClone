from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import relationship
from models.base import Base


class Thread(Base):
    __tablename__ = 'threads'
    thread_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    date_of_creation = Column(Date)
    posts = relationship("Post", back_populates="thread", cascade="all, delete, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="thread", cascade="all, delete, delete-orphan")
