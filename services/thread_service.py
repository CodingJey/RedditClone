from sqlalchemy.ext.asyncio import AsyncSession
from repositories.repository import (
    create_user, get_user, list_users, update_user, delete_user, get_user_by_email
)
from repositories.repository import create_thread, get_thread, list_threads, delete_thread
from repositories.repository import create_post, list_posts, delete_post
from schemas.schemas import UserCreate, UserUpdate, ThreadCreate, PostCreate

# Thread Service Functions

async def create_thread_service(db: AsyncSession, thread: ThreadCreate):
    """Create a new thread entry in the database."""
    return await create_thread(db, thread)

async def get_thread_service(db: AsyncSession, thread_id: int):
    """Retrieve a single thread by its ID."""
    return await get_thread(db, thread_id)

async def list_threads_service(db: AsyncSession, skip: int = 0, limit: int = 10):
    """Retrieve a list of threads with optional pagination."""
    return await list_threads(db, skip, limit)

async def delete_thread_service(db: AsyncSession, thread_id: int):
    """Delete a thread entry from the database."""
    return await delete_thread(db, thread_id)
