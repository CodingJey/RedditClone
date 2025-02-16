from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'
    subscription_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    thread_id = Column(Integer, ForeignKey('threads.thread_id'))
    subscription_date = Column(Date)
    user = relationship("User", back_populates="subscriptions")
    thread = relationship("Thread", back_populates="subscriptions")
