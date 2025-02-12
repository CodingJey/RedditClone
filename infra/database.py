from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL
import asyncpg
import os

# Configuration for database URLs
EXTERNAL_DATABASE_URL = os.getenv("DATABASE_URL","postgresql+asyncpg://appadmin:admin@db:5432/appdb")
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

async def is_db_reachable(connection_url: str) -> bool:
    """Check if PostgreSQL database is reachable using parsed connection URL"""
    try:
        # Parse the connection URL
        url = URL.create(connection_url)
        conn = await asyncpg.connect(
        host="db", 
        port=5432,
        user="appadmin",
        password="admin",
        database="appdb",
        timeout=3
        )
        print("test connection works")
        await conn.close()
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

async def init_engine():
    """Initialize database engine with proper error handling"""
    try:
        # First check if database is reachable
        if await is_db_reachable(EXTERNAL_DATABASE_URL):
            # Create engine with connection validation
            engine = create_async_engine(
                EXTERNAL_DATABASE_URL,
                future=True,
                echo=True,
                pool_pre_ping=True  # Check connections before using them
            )
            
            # Test connection immediately
            
            print("Connected to the external PostgreSQL database.")
            return engine
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")

    # Fallback to SQLite
    print("Falling back to the test database.")
    return create_async_engine(TEST_DATABASE_URL, future=True, echo=True)

# Session factory setup
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=None,  # Set after engine initialization
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency injection
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Database initialization
async def init_db():
    engine = await init_engine()  # Get initialized engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Application startup
async def startup():
    global engine, AsyncSessionLocal
    engine = await init_engine()
    AsyncSessionLocal.configure(bind=engine)

