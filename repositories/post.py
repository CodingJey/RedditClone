from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import User, Thread, Post
from schemas.schemas import UserCreate, UserUpdate, ThreadCreate, PostCreate
from datetime import datetime

# Post Repository Functions

async def create_post(db: AsyncSession, thread_id: int, post_create: PostCreate):
    """Create a new post in the specified thread."""
    db_thread = await get_thread(db, thread_id)
    if db_thread:
        db_post = Post(
            thread_id=thread_id,
            poster_id=post_create.poster_id,
            content=post_create.content,
            name=post_create.name
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    return None

async def list_posts(db: AsyncSession, thread_id: int, skip: int = 0, limit: int = 10):
    """Retrieve posts in a thread with pagination."""
    db_thread = await get_thread(db, thread_id)
    if db_thread:
        return db.query(Post).filter(Post.thread_id == thread_id).offset(skip).limit(limit).all()
    return []

async def delete_post(db: AsyncSession, thread_id: int, post_id: int):
    """Delete a post by post_id in the specified thread."""
    db_post = await db.query(Post).filter(Post.thread_id == thread_id, Post.post_id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False
