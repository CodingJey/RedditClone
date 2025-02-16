from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repository import UserRepository
from schemas.user_model import UserCreateRequest,UserUpdateRequest

# User Service Functions
class UserService():
    def __init__(self, user_repository: UserRepository):
        self.repo = user_repository
    
    async def create_user_service(db: AsyncSession, user: UserCreateRequest):
        """Create a new user entry in the database."""
        print(**user.modelDump())
        return await self.repo.create_user(db, **user.modelDump())

    async def get_user_service(db: AsyncSession, user_id: int):
        """Retrieve a single user by its ID."""
        return await self.repo.get_user_by_id(db, user_id)

    async def list_users_service(db: AsyncSession, skip: int = 0, limit: int = 10):
        """Retrieve a list of users with optional pagination."""
        return await self.repo.list_users(db, skip, limit)

    async def update_user_service(db: AsyncSession, user_id: int, user: UserUpdateRequest):
        """Update an existing user entry in the database."""
        return await self.repo.update_user(db, user_id, user)

    async def delete_user_service(db: AsyncSession, user_id: int):
        """Delete a user entry from the database."""
        return await self.repo.delete_user(db, user_id)

    async def get_user_by_email_service(db: AsyncSession, email: str):
        """Retrieve a user by email."""
        return await self.repo.get_user_by_email(db, email)
