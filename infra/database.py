
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
import asyncpg
import asyncio
import os

# Configuration for database URLs
EXTERNAL_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://appadmin:admin@localhost:5432/appdb")
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Function to check if the database is reachable
async def is_db_reachable(connection_url: str) -> bool:
    try:
        parsed_url = asyncpg.parse_connect_dsn(connection_url)
        conn = await asyncpg.connect(
            host=parsed_url.host,
            port=parsed_url.port,
            user=parsed_url.user,
            password=parsed_url.password,
            database=parsed_url.database,
            timeout=3
        )
        await conn.close()
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

# Initialize the database engine
async def init_engine():
    try:
        if await is_db_reachable(EXTERNAL_DATABASE_URL):
            engine = create_async_engine(EXTERNAL_DATABASE_URL, future=True, echo=True)
            print("Connected to the external PostgreSQL database.")
        else:
            raise ConnectionError("Database connection timeout or unreachable.")
    except Exception as e:
        print(f"Failed to connect to external PostgreSQL database: {e}. Falling back to the test database.")
        engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
    return engine

# Create the async session factory
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=None,  # Will be set after engine initialization
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency to get a database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Initialize the database (create tables)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# For testing: Create an in-memory SQLite database
async def get_test_db():
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True, echo=True)
    TestAsyncSessionLocal = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
        class_=AsyncSession
    )
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestAsyncSessionLocal() as session:
        yield session

# Initialize the engine and bind it to the session factory
async def startup():
    global engine, AsyncSessionLocal
    engine = await init_engine()
    AsyncSessionLocal.configure(bind=engine)

