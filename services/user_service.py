from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repository import UserRepository, get_user_repository
from schemas.user_model import UserCreateRequest,UserUpdateRequest, UserResponse
from fastapi import Depends 

# User Service Functions
class UserService():
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def create_user_service(self, db: AsyncSession, req: UserCreateRequest ) -> UserResponse:
        """Create a new user entry in the database."""
        return await self.user_repository.create_user(req)

    async def get_user_service(self, db: AsyncSession, user_id: int):
        """Retrieve a single user by its ID."""
        return await self.user_repository.get_user_by_id(user_id)

    async def list_users_service(self, db: AsyncSession, skip: int = 0, limit: int = 10):
        """Retrieve a list of users with optional pagination."""
        return await self.user_repository.list_users(skip, limit)

    async def update_user_service(self, db: AsyncSession, user_id: int, user: UserUpdateRequest):
        """Update an existing user entry in the database."""
        return await self.user_repository.update_user(user_id, user)

    async def delete_user_service(self, db: AsyncSession, user_id: int):
        """Delete a user entry from the database."""
        return await self.user_repository.delete_user(user_id)

    async def get_user_by_email_service(self, db: AsyncSession, email: str):
        """Retrieve a user by email."""
        return await self.user_repository.get_user_by_email(email)


async def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repo)