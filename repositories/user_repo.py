from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.user_model import UserCreate, UserUpdate, User, UserResponse
# User Repository Functions


class UserRepository(BaseRepository):

    async def create_user(self, session: AsyncSession, user : User) -> UserResponse:
        user = User(**user.modelDump())
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> User | None:
        result = await session.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def update_user_email(self, session: AsyncSession, user_id: int, new_email: str) -> User | None:
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(email=new_email)
        )
        return await self.get_user_by_id(user_id)

    async def deactivate_user(self, session: AsyncSession, user_id: int) -> None:
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_active=False)
        )

    async def list_active_users(self, session: AsyncSession) -> list[User]:
        result = await session.execute(
            select(User).where(User.is_active == True)
        )
        return result.scalars().all()