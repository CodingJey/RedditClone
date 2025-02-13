from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.userModel import UserCreate, UserUpdate,User
# User Repository Functions

async def create_user(db: AsyncSession, user_create: UserCreate):
    """Create a new user in the database."""
    db_user : User = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        nickname=user_create.nickname,
        date_of_birth=user_create.date_of_birth,
        # date_of_joining=datetime.datetime.now(),
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
