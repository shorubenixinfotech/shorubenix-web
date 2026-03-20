from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from config.database import execute_query
from middleware.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/blog", tags=["Blog"])


class BlogPostCreate(BaseModel):
    title: str
    excerpt: str | None = None
    content: str | None = None
    author: str = "ShoRubenix"
    tags: list[str] = []
    image_url: str | None = None
    read_time: str | None = None


@router.get("")
async def get_blog_posts():
    posts = execute_query("SELECT * FROM blog_posts WHERE is_published = TRUE ORDER BY created_at DESC", fetch_all=True)
    return {"posts": posts}


@router.get("/{post_id}")
async def get_blog_post(post_id: int):
    # Increment views
    execute_query("UPDATE blog_posts SET views = views + 1 WHERE id = %s", (post_id,))
    
    post = execute_query("SELECT * FROM blog_posts WHERE id = %s", (post_id,), fetch_one=True)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {"post": post}


@router.post("")
async def create_blog_post(data: BlogPostCreate, current_user=Depends(get_current_user)):
    import json
    slug = data.title.lower().replace(" ", "-").replace("'", "")
    
    post = execute_query(
        """
        INSERT INTO blog_posts 
        (title, slug, content, excerpt, author, tags, image_url, is_published, published_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE, CURRENT_TIMESTAMP) 
        RETURNING *
        """,
        (data.title, slug, data.content, data.excerpt, data.author, json.dumps(data.tags), data.image_url),
        fetch_one=True
    )
    
    return {"message": "Blog post created", "post": post}
