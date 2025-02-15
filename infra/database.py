from __future__ import annotations
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, TypeVar, Callable, Coroutine, ParamSpec, Concatenate
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL, select, update
import asyncpg
import os

P = ParamSpec("P")
R = TypeVar("R")

EXTERNAL_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://appadmin:admin@db:5432/appdb")
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Database:
    def __init__(self, url: str | None = None):
        self.url = url or EXTERNAL_DATABASE_URL
        self.engine = None
        self.async_session_local = None

    async def is_db_reachable(self) -> bool:
        """Keep connectivity check but make it instance method"""
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
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    async def startup(self) -> None:
        """Consolidated initialization"""
        try:
            if await self.is_db_reachable():
                self.engine = create_async_engine(
                    self.url,
                    future=True,
                    echo=True,
                    pool_pre_ping=True
                )
                print("Connected to PostgreSQL database.")
            else:
                raise RuntimeError("Primary database unreachable")
        except Exception as e:
            print(f"Falling back to SQLite: {e}")
            self.engine = create_async_engine(
                TEST_DATABASE_URL,
                future=True,
                echo=True
            )

        self.async_session_local = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def session_scope(self) -> AsyncSession:
        """Keep as main session provider"""
        if not self.async_session_local:
            raise RuntimeError("Database not initialized")

        async with self.async_session_local() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

