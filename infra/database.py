from __future__ import annotations
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, TypeVar, Callable, Coroutine, ParamSpec, Concatenate, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import URL, select, update
import asyncpg
import os
import logging
from fastapi import Depends

logger = logging.getLogger("app")  # Get logger instance

P = ParamSpec("P")
R = TypeVar("R")

EXTERNAL_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://appadmin:admin@db:5432/appdb")
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

Base = declarative_base()

class Database:
    _instance: Optional[Database] = None

    def __new__(cls, url: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.url = url or EXTERNAL_DATABASE_URL
            cls._instance.engine = None
            cls._instance.async_session_local = None
            cls._instance._is_initialized = False
        return cls._instance

    def __init__(self, url: Optional[str] = None):
        if self.engine is not None:
            return # Prevent re-initialization

    async def _is_db_reachable(self) -> bool:
        """Connectivity check, now private method.""" # Corrected docstring
        try:
            url_obj = URL.create(self.url)
            if url_obj.drivername != 'postgresql+asyncpg':
                return True

            conn = await asyncpg.connect(
                host=url_obj.host or "localhost",
                port=url_obj.port or 5432,
                user=url_obj.username,
                password=url_obj.password,
                database=url_obj.database,
                timeout=3
            )
            await conn.close()
            logger.info("Database is reachable.") # Keep info level for reachability success
            return True
        except Exception as e:
            url_obj = URL.create(self.url)
            db_details = {
                "host": url_obj.host or "localhost",
                "port": url_obj.port or 5432,
                "username": url_obj.username,
                "database": url_obj.database,
            }
            logger.error(
                "DB connection error to: Host=%(host)s, Port=%(port)s, User=%(username)s, DB=%(database)s. Error: %(error)s",
                db_details | {"error": e}, # Merging db_details and error into a single dict for logging
                exc_info=True,
            )
            return False

    async def initialize(self) -> None:
        """Initializes the database engine and session maker if not already initialized.""" # Corrected docstring
        if self._is_initialized:
            return # Prevent re-initialization

        try:
            if await self._is_db_reachable():
                self.engine = create_async_engine(
                    self.url,
                    future=True,
                    echo=False, # Keep echo False for production, enable in specific cases
                    pool_pre_ping=True
                )
                self.async_session_local = async_sessionmaker(
                    bind=self.engine,
                    autocommit=False,
                    autoflush=False,
                    expire_on_commit=False,
                    class_=AsyncSession
                )
                logger.info("Connected to PostgreSQL database and SessionLocal created.") # More informative log
            else:
                raise RuntimeError("Primary database unreachable") # More specific error message for primary DB
        except Exception as e:
            logger.error("Error during PostgreSQL startup: %s", e, exc_info=True) # More specific log for PostgreSQL error
            logger.info("Falling back to SQLite...") # Keep info for fallback message
            self.url = TEST_DATABASE_URL # Fallback to SQLite URL
            try:
                self.engine = create_async_engine(
                    self.url,
                    future=True,
                    echo=False, # Keep echo False for production, enable in specific cases
                    pool_pre_ping=True
                )
                self.async_session_local = async_sessionmaker(
                    bind=self.engine,
                    autocommit=False,
                    autoflush=False,
                    expire_on_commit=False,
                    class_=AsyncSession
                )
                logger.info("Successfully initialized SQLite fallback database.") # Log fallback success
            except Exception as sqlite_e:
                logger.error("Error during SQLite fallback startup: %s", sqlite_e, exc_info=True) # More specific log for SQLite error
                raise RuntimeError(f"Failed to initialize databases: {sqlite_e}") from e # More informative error message
            raise RuntimeError("Primary PostgreSQL database unreachable during startup, fallback to SQLite initialized.") from e # More informative error message
        finally:
            self._is_initialized = True # Ensure flag is set regardless of success/failure


database_instance = Database() # Create the singleton instance

# Dependency function to get the *initialized* Database instance
def get_database() -> Database:  # Renamed to get_database
    """Dependency to provide the *initialized* Database instance.""" # Corrected docstring
    return database_instance # Return the global singleton instance


# Dependency function to get the session using session_scope and Database instance
async def get_session(database: Database = Depends(get_database)) -> AsyncSession:
    """Dependency to provide a database session.""" # Corrected docstring
    async with session_scope(database) as session: # Use session_scope with the injected Database instance
        yield session

@asynccontextmanager
async def session_scope(database_instance: Database = Depends(get_database)) -> AsyncSession:
    """Session provider that needs a Database instance.""" # Corrected docstring
    if not database_instance.async_session_local:
        raise RuntimeError("Database not initialized for session_scope") # More informative error

    async with database_instance.async_session_local() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error("Session scope error, rolling back: %s", e, exc_info=True) # Log session scope errors
            await session.rollback()
            raise
