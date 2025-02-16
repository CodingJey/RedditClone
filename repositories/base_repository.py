from sqlalchemy.ext.asyncio import AsyncSession
from infra import database

class BaseRepository:
    """Base repository class with database access."""
    def __init__(self, session: AsyncSession):
        self.session = session
