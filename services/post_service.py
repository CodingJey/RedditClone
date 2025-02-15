from sqlalchemy.ext.asyncio import AsyncSession
from repositories.post import create_post, list_posts, delete_post
from models.post_model import Post, PostCreate

class PostService():
    def __init__(self, repo:Post)

    async def create_post_service(db: AsyncSession, thread_id: int, post: PostCreate):
        """Create a new post entry in the specified thread."""
        return await create_post(db, thread_id, post)

    async def list_posts_service(db: AsyncSession, thread_id: int, skip: int = 0, limit: int = 10):
        """Retrieve a list of posts in a thread with optional pagination."""
        return await list_posts(db, thread_id, skip, limit)

    async def delete_post_service(db: AsyncSession, thread_id: int, post_id: int):
        """Delete a post entry from the specified thread."""
        return await delete_post(db, thread_id, post_id)
