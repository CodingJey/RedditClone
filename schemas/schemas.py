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
    # date_of_joining: date

    model_config = ConfigDict(from_attributes=True)



