from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
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
    posts = relationship("Post", back_populates="poster", cascade="all, delete, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete, delete-orphan")

class Thread(Base):
    __tablename__ = 'threads'
    thread_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    date_of_creation = Column(Date)
    posts = relationship("Post", back_populates="thread", cascade="all, delete, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="thread", cascade="all, delete, delete-orphan")

class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey('threads.thread_id'), index=True)
    poster_id = Column(Integer, ForeignKey('users.user_id'), index=True)
    content = Column(String)
    post_date = Column(Date)
    rating = Column(Integer, default=0)
    thread = relationship("Thread", back_populates="posts")
    poster = relationship("User", back_populates="posts")

class Subscription(Base):
    __tablename__ = 'subscriptions'
    subscription_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    thread_id = Column(Integer, ForeignKey('threads.thread_id'))
    subscription_date = Column(Date)
    user = relationship("User", back_populates="subscriptions")
    thread = relationship("Thread", back_populates="subscriptions")
