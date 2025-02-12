from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date

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