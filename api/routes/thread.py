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


@router.get("/threads", response_model=list[Thread])
async def list_threads(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    threads = await list_threads_service(db, skip, limit)
    return threads

@router.post("/threads", response_model=Thread, status_code=201)
async def create_thread(thread_data: ThreadCreate, db: AsyncSession = Depends(get_db)):
    thread = await create_thread_service(db, thread_data)
    return thread

@router.get("/threads/{thread_id}/posts", response_model=list[Post])
async def list_posts(thread_id: int, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    posts = await list_posts_service(db, thread_id, skip, limit)
    if not posts:
        raise HTTPException(status_code=404, detail="Thread not found or no posts")
    return posts

@router.post("/threads/{thread_id}/posts", response_model=Post, status_code=201)
async def create_post(thread_id: int, post_data: PostCreate, db: AsyncSession = Depends(get_db)):
    post = await create_post_service(db, thread_id, post_data)
    if not post:
        raise HTTPException(status_code=404, detail="Thread not found")
    return post

@router.delete("/threads/{thread_id}/posts/{post_id}", response_model=dict)
async def delete_post(thread_id: int, post_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_post_service(db, thread_id, post_id):
        raise HTTPException(status_code=404, detail="Post not found or does not belong to the specified thread")
    return {"detail": "Post deleted successfully"}