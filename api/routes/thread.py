# from fastapi import APIRouter, Depends, HTTPException, Header
# from sqlalchemy.ext.asyncio import AsyncSession
# from schemas.threadModel import (
#     ThreadCreate, Thread
# )
# from services.thread_service import (
#     list_threads_service, create_thread_service
# )
# from infra.database import get_db

# router = APIRouter()


# @router.get("/threads", response_model=list[Thread])
# async def list_threads(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
#     threads = await list_threads_service(db, skip, limit)
#     return threads

# @router.post("/threads", response_model=Thread, status_code=201)
# async def create_thread(thread_data: ThreadCreate, db: AsyncSession = Depends(get_db)):
#     thread = await create_thread_service(db, thread_data)
#     return thread
