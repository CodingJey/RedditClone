from sqlalchemy.ext.asyncio import AsyncSession
from schemas.thread_model import Thread, ThreadCreate
from datetime import datetime

# Thread Repository Functions
class ThreadRepository():

    async def create_thread(self, thread_create: ThreadCreate) -> Thread:
        """Create a new thread in the database."""
        db_thread = Thread(**ThreadCreate.modelDump())
        await db.add(db_thread)
        db.commit()
        db.refresh(db_thread)
        return db_thread

    async def get_thread(db: AsyncSession, thread_id: int):
        """Retrieve a thread by thread_id."""
        return await db.query(Thread).filter(Thread.thread_id == thread_id).first()

    async def list_threads(db: AsyncSession, skip: int = 0, limit: int = 10):
        """Retrieve a list of threads with pagination."""
        return await db.query(Thread).offset(skip).limit(limit).all()

    async def delete_thread(db: AsyncSession, thread_id: int):
        """Delete a thread by thread_id and cascade delete associated posts."""
        db_thread = await get_thread(db, thread_id)
        if db_thread:
            db.delete(db_thread)
            db.commit()
            return True
        return False
