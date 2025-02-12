from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import User, Thread, Post
from schemas.schemas import UserCreate, UserUpdate, ThreadCreate, PostCreate
from datetime import datetime





# Additional Function for Authentication

async def get_user_by_email(db: AsyncSession, email: str):
    """Retrieve a user by email."""
    return await db.query(User).filter(User.email == email).first()
