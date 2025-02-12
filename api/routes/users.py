from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import (
    LoginRequest, LoginResponse, UserCreate, UserUpdate, User,
    ThreadCreate, Thread, PostCreate, Post
)
from services.service import (
    list_users_service, create_user_service,
    get_user_service, update_user_service, delete_user_service,
    list_threads_service, create_thread_service,
    list_posts_service, create_post_service, delete_post_service
)
# from services.service import (login_service, logout_service) 
from fastapi.responses import Response
from infra.database import get_db


@router.get("/users", response_model=list[User])
async def list_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await list_users_service(db, skip, limit)
    return users

@router.post("/users",response_model=User ,status_code=201)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user_service(db, user_data)

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_service(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await update_user_service(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_user_service(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
