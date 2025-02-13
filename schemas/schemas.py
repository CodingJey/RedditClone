from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str





