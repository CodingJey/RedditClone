from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import User, Thread, Post
from schemas.schemas import UserCreate, UserUpdate, ThreadCreate, PostCreate
from datetime import datetime
# User Repository Functions

async def create_user(db: AsyncSession, user_create: UserCreate):
    """Create a new user in the database."""
    db_user : User = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        nickname=user_create.nickname,
        date_of_birth=user_create.date_of_birth,
        email=user_create.email,
        password=user_create.password  # Assume password hashing is handled elsewhere
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user(db: AsyncSession, user_id: int):
    """Retrieve a user by user_id."""
    return await db.query(User).filter(User.user_id == user_id).first()

async def list_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    """Update user details by user_id."""
    db_user = await get_user(db, user_id)
    if db_user:
        if user_update.name:
            db_user.name = user_update.name
        if user_update.email:
            db_user.email = user_update.email
        db.commit()
        db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    """Delete a user by user_id and cascade delete associated posts."""
    db_user = await get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# Thread Repository Functions

async def create_thread(db: AsyncSession, thread_create: ThreadCreate):
    """Create a new thread in the database."""
    db_thread = Thread(
        name=thread_create.name,
        description=thread_create.description
    )
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

# Additional Function for Authentication

async def get_user_by_email(db: AsyncSession, email: str):
    """Retrieve a user by email."""
    return await db.query(User).filter(User.email == email).first()
