from typing import AsyncGenerator, Callable
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.base_repository import BaseRepository

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.session_scope() as session:
        yield session

def get_repository(repo_type: type[BaseRepository]) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(session: AsyncSession = Depends(get_session)) -> BaseRepository:
        return repo_type(session)
    return _get_repo

