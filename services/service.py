from sqlalchemy.ext.asyncio import AsyncSession
from repositories.repository import (
    create_user, get_user, list_users, update_user, delete_user, get_user_by_email
)
from repositories.repository import create_thread, get_thread, list_threads, delete_thread
from repositories.repository import create_post, list_posts, delete_post
from schemas.schemas import UserCreate, UserUpdate, ThreadCreate, PostCreate

# User Service Functions

async def create_user_service(db: AsyncSession, user: UserCreate):
    """Create a new user entry in the database."""
    return await create_user(db, user)

async def get_user_service(db: AsyncSession, user_id: int):
    """Retrieve a single user by its ID."""
    return await get_user(db, user_id)

async def list_users_service(db: AsyncSession, skip: int = 0, limit: int = 10):
    """Retrieve a list of users with optional pagination."""
    return await list_users(db, skip, limit)

async def update_user_service(db: AsyncSession, user_id: int, user: UserUpdate):
    """Update an existing user entry in the database."""
    return await update_user(db, user_id, user)

async def delete_user_service(db: AsyncSession, user_id: int):
    """Delete a user entry from the database."""
    return await delete_user(db, user_id)

async def get_user_by_email_service(db: AsyncSession, email: str):
    """Retrieve a user by email."""
    return await get_user_by_email(db, email)

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

# Post Service Functions

async def create_post_service(db: AsyncSession, thread_id: int, post: PostCreate):
    """Create a new post entry in the specified thread."""
    return await create_post(db, thread_id, post)

async def list_posts_service(db: AsyncSession, thread_id: int, skip: int = 0, limit: int = 10):
    """Retrieve a list of posts in a thread with optional pagination."""
    return await list_posts(db, thread_id, skip, limit)

async def delete_post_service(db: AsyncSession, thread_id: int, post_id: int):
    """Delete a post entry from the specified thread."""
    return await delete_post(db, thread_id, post_id)
