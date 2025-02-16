from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional, ClassVar

class UserRequest(BaseModel):
    user_id: int
    first_name : str
    last_name : str
    nickname : str
    email: str
    password : str
    date_of_birth : date
    is_active : str 

    model_config: ClassVar[dict] = {"from_attributes": True} # Correct way to set Config in Pydantic v2+


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

    model_config: ClassVar[dict] = {"from_attributes": True} # Correct way to set Config in Pydantic v2+

class UserUpdateRequest(BaseModel):
    name: str = Field(None)
    email: str = Field(None, description="Must be a valid email address")
    
    model_config: ClassVar[dict] = {"from_attributes": True} # Correct way to set Config in Pydantic v2+

