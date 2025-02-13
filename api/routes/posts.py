from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.postModel import (
    PostCreate, Post
)
from services.post_service import (
    list_posts_service, create_post_service, delete_post_service
)
from infra.database import get_db

router = APIRouter()

@router.get("/threads/{thread_id}/posts", response_model=list[Post])
async def list_posts(thread_id: int, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    posts = await list_posts_service(db, thread_id, skip, limit)
    if not posts:
        raise HTTPException(status_code=404, detail="Thread not found or no posts")
    return posts

@router.post("/threads/{thread_id}/posts", response_model=Post, status_code=201)
async def create_post(thread_id: int, post_data: PostCreate, db: AsyncSession = Depends(get_db)):
    post = await create_post_service(db, thread_id, post_data)
    return post

@router.delete("/threads/{thread_id}/posts/{post_id}", response_model=dict)
async def delete_post(thread_id: int, post_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_post_service(db, thread_id, post_id):
        raise HTTPException(status_code=404, detail="Post not found or does not belong to the specified thread")
    return {"detail": "Post deleted successfully"}
