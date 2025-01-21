from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str

class User(BaseModel):
    user_id: int
    first_name : str 
    last_name : str 
    nickname : str 
    email: str
    password : str
    date_of_birth : date 
    date_of_joining: date

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    nickname: str
    date_of_birth: date
    email: str
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str = Field(None)
    email: str = Field(None, description="Must be a valid email address")
    class Config:
        orm_mode = True
class Thread(BaseModel):
    thread_id: int
    name: str
    description: str
    date_of_creation: date

class ThreadCreate(BaseModel):
    name: str
    description: str
    class Config:
        orm_mode = True
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
