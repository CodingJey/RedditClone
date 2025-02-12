from sqlalchemy.ext.asyncio import AsyncSession
from repositories.repository import (
    create_user, get_user, list_users, update_user, delete_user, get_user_by_email
)
from repositories.repository import create_thread, get_thread, list_threads, delete_thread
from repositories.repository import create_post, list_posts, delete_post
from schemas.schemas import UserCreate, UserUpdate, ThreadCreate, PostCreate



async def create_post_service(db: AsyncSession, thread_id: int, post: PostCreate):
    """Create a new post entry in the specified thread."""
    return await create_post(db, thread_id, post)

async def list_posts_service(db: AsyncSession, thread_id: int, skip: int = 0, limit: int = 10):
    """Retrieve a list of posts in a thread with optional pagination."""
    return await list_posts(db, thread_id, skip, limit)

async def delete_post_service(db: AsyncSession, thread_id: int, post_id: int):
    """Delete a post entry from the specified thread."""
    return await delete_post(db, thread_id, post_id)
