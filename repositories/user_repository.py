from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.User import User
from schemas.user_model import UserCreateRequest, UserResponse
from repositories.base_repository import BaseRepository
from infra.database import session_scope
from fastapi import Depends 
from datetime import datetime

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        # super().__init__(session)
        self.session = session
        self.model = User

    async def create_user(self, req: UserCreateRequest) -> UserResponse: # Corrected type hint to UserResponse
        user: User = User( first_name = req.first_name,
                            last_name = req.last_name,
                            nickname = req.nickname,
                            password = req.password,
                            email = req.email,
                            date_of_birth = req.date_of_birth,
                            is_active = True) # Corrected: Python boolean True

        await self.session.add(user)
        await self.session.flush() # flush to get the generated id right after adding
        await self.session.refresh(user) # refresh to load any database-generated defaults and the id

        user_response = UserResponse( 
                                    user_id = user.user_id,
                                    first_name = user.first_name,
                                    last_name = user.last_name,
                                    nickname = user.nickname,
                                    email = user.email,
                                    date_of_birth = user.date_of_birth)
        return user_response


    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def update_user_email(self, user_id: int, new_email: str) -> User | None:
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(email=new_email)
        )
        return await self.get_user_by_id(user_id)

    async def deactivate_user(self,  user_id: int) -> None:
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_active=False)
        )

    async def list_active_users(self) -> list[User]:
        result = await self.session.execute(
            select(User).where(User.is_active == True)
        )
        return result.scalars().all()

async def get_user_repository(
    session: AsyncSession = Depends(session_scope)
) -> UserRepository:
    """Dependency to get UserRepository."""
    return UserRepository(session)