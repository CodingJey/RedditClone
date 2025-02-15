from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user import (
    create_user, get_user, list_users, update_user, delete_user, get_user_by_email
)
from schemas.userModel import UserCreate,UserUpdate

# User Service Functions
class UserService():
    
    async def create_user_service(db: AsyncSession, user: UserCreate):
        """Create a new user entry in the database."""
        return await create_user(db, user)

    async def get_user_service(db: AsyncSession, user_id: int):
        """Retrieve a single user by its ID."""
        return await get_user(db, user_id)

    async def list_users_service(db: AsyncSession, skip: int = 0, limit: int = 10):
        """Retrieve a list of users with optional pagination."""
        return await list_users(db, skip, limit)

    async def update_user_service(db: AsyncSession, user_id: int, user: UserUpdate):
        """Update an existing user entry in the database."""
        return await update_user(db, user_id, user)

    async def delete_user_service(db: AsyncSession, user_id: int):
        """Delete a user entry from the database."""
        return await delete_user(db, user_id)

    async def get_user_by_email_service(db: AsyncSession, email: str):
        """Retrieve a user by email."""
        return await get_user_by_email(db, email)
