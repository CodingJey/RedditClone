from typing import AsyncGenerator
from fastapi import Depends
from repositories import BaseRepository, user_repo

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.session_scope() as session:
        yield session

def get_repository(repo_type: type[BaseRepository]) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(session: AsyncSession = Depends(get_session)) -> BaseRepository:
        return repo_type(session)
    return _get_repo

def get_user_service(
    user_repo: UserRepository = Depends(get_repository(user_repo))
) -> UserService:
    return UserService(user_repo)