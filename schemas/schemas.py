from pydantic import BaseModel, Field
from typing import Optional

# Schema for reading a product (response model)
class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy ORM objects


# Schema for creating or updating a product (request model)
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1024)
    price: float = Field(..., gt=0)

    class Config:
        orm_mode = True

