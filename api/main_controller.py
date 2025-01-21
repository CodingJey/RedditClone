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

router = APIRouter()
#
# def get_token(authorization: str = Header(...)):
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Invalid authorization header")
#     return authorization[len("Bearer "):]
#
# @router.post("/login", response_model=LoginResponse)
# async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
#     token = await login_service(db, login_data.email, login_data.password)
#     if not token:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return {"token": token}
#
# @router.post("/logout")
# async def logout(token: str = Depends(get_token), db: AsyncSession = Depends(get_db)):
#     await logout_service(db, token)
#     return Response(status_code=204)

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
