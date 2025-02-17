from __future__ import annotations

import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import asyncpg
from fastapi import Depends
from sqlalchemy import URL, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger("app")

EXTERNAL_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://appadmin:admin@localhost:5432/appdb")
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

Base = declarative_base()


class Database:
    _instance: Optional[Database] = None
    url: str
    engine: create_async_engine
    async_session_local: async_sessionmaker

    def __new__(cls, url: Optional[str] = None) -> Database:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, url: Optional[str] = None) -> None:
        if hasattr(self, 'engine') and self.engine is not None:  # Check if already initialized
            return

        self.url = url or EXTERNAL_DATABASE_URL
        self.engine = None
        self.async_session_local = None
        self._is_initialized = False
        self._initialize_sync() # Initialize synchronously once upon instance creation

    def _initialize_sync(self) -> None:
        """Synchronously initializes the database engine and session maker."""
        try:
            if self._is_db_reachable_sync():
                self._create_engine_and_session()
            else:
                self._fallback_to_sqlite()
        except Exception as e:
            logger.exception("Database initialization error")
            self._fallback_to_sqlite(original_exception=e)
        finally:
            self._is_initialized = True


    def _create_engine_and_session(self) -> None:
        """Creates the SQLAlchemy engine and session maker."""
        self.engine = create_async_engine(
            self.url,
            future=True,
            echo=False,
            pool_pre_ping=True
        )
        self.async_session_local = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )
        logger.info(f"Connected to database: {self.url}")


    def _fallback_to_sqlite(self, original_exception: Optional[Exception] = None) -> None:
        """Falls back to SQLite database."""
        sqlite_url = TEST_DATABASE_URL
        try:
            self.url = sqlite_url
            self._create_engine_and_session()
            logger.info("Fallback to SQLite successful.")
        except Exception as sqlite_e:
            if original_exception:
                msg = f"Failed to initialize primary DB and SQLite fallback. Original error: {original_exception}, SQLite error: {sqlite_e}"
            else:
                msg = f"Failed to initialize SQLite fallback. Error: {sqlite_e}"
            logger.exception(msg)
            raise RuntimeError(msg) from sqlite_e


    def _is_db_reachable_sync(self) -> bool:
        """Connectivity check using asyncpg directly for PostgreSQL."""
        try:
            url_obj = URL.create(self.url)
            if url_obj.drivername != 'postgresql+asyncpg': # Short circuit for non-postgresql
                return True

            async def _async_check(): # Define an async function inside sync method for asyncpg connection
                conn = None
                try:
                    conn = await asyncpg.connect(
                        host=url_obj.host or "localhost",
                        port=url_obj.port or 5432,
                        user=url_obj.username,
                        password=url_obj.password,
                        database=url_obj.database,
                        timeout=3
                    )
                    return True
                except Exception:
                    return False
                finally:
                    if conn:
                        await conn.close()

            if not create_engine(self.url).url.get_driver_name() == 'postgresql+asyncpg':
                return True # Skip asyncpg check for non-postgresql dbs

            import asyncio # Import asyncio inside the sync function to run async code
            if asyncio.run(_async_check()):
                logger.info("Database is reachable.")
                return True
            else:
                db_details = {
                    "host": url_obj.host or "localhost",
                    "port": url_obj.port or 5432,
                    "username": url_obj.username,
                    "database": url_obj.database,
                }
                logger.error(
                    "DB connection error to: Host=%(host)s, Port=%(port)s, User=%(username)s, DB=%(database)s.",
                    db_details,
                    exc_info=True,
                )
                return False

        except Exception:
            logger.exception("Error during database reachability check.")
            return False


database_instance = Database()

def get_database() -> Database:
    return database_instance

@asynccontextmanager
async def session_scope(database: Database = Depends(get_database)) -> AsyncGenerator[AsyncSession, None]:
    """Provides a database session with commit and rollback on exceptions."""
    if not database.async_session_local:
        raise RuntimeError("Database not initialized for session_scope")

    session = database.async_session_local()
    try:
        yield session
        await session.commit()
    except Exception:
        logger.exception("Session scope error, rolling back transaction.")
        await session.rollback()
        raise

async def get_session(database: Database = Depends(get_database)) -> AsyncGenerator[AsyncSession, None]:
    async with session_scope(database) as session:
        yield session