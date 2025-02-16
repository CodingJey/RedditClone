from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional

class UserRequest(BaseModel):
    user_id: int
    first_name : str
    last_name : str
    nickname : str
    email: str
    password : str
    date_of_birth : date
    date_of_joining: date
    is_active : str = Field(None)  

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    user_id: int
    first_name : str
    last_name : str
    nickname : str
    email: str
    date_of_birth : date


class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    nickname: str
    date_of_birth: date
    email: str
    password: str

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    name: str = Field(None)
    email: str = Field(None, description="Must be a valid email address")
    
    class Config:
        from_attributes = True
