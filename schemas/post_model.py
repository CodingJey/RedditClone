from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date

class Post(BaseModel):
    post_id: int
    thread_id: int
    poster_id: int
    content: str
    post_date: date
    rating: int = 0

class PostCreate(BaseModel):
    thread_id: int
    poster_id: int
    content: str
    name: str
    class Config:
        orm_mode = True
