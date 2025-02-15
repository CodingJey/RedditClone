from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date

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