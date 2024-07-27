from fastapi import APIRouter, Depends, HTTPException
from .models import ShowPost, CreatePost, UpdatePost
from db.session import get_db
from db.operations import PostController
from sqlalchemy.ext.asyncio import AsyncSession

post_router = APIRouter(tags=['Posts_controller'])

async def new_post(body: CreatePost, db):
    async with db as session:
        async with session.begin():
            post_cont = PostController(session)
            post = await post_cont.create(body)
            return ShowPost(
                id=post.id,
                title=post.title,
                post_image=post.post_image,
                content=post.content,
                owner_id=post.owner_id
            )
        
async def posts_get_all(db):
    async with db as session:
        async with session.begin():
            post_cont = PostController(session)
            posts = await post_cont.post_list()
            return posts
        
async def posts_get_one(id: int, db):
    async with db as session:
        async with session.begin():
            post_cont = PostController(session)
            posts = await post_cont.post_detail(id)
            return posts
        
async def post_delete(id: int, db):
    async with db as session:
        async with session.begin():
            post_cont = PostController(session)
            return await post_cont.post_detail_delete(id)
        
async def post_update(id: int, body: UpdatePost, db):
    async with db as session:
        async with session.begin():
            post_cont = PostController(session)
            upd_post = await post_cont.post_detail_update(id, body)
            return upd_post
        
        
@post_router.post("/posts", response_model=ShowPost)
async def creating(body: CreatePost, db: AsyncSession = Depends(get_db)):
    return await new_post(body, db)

@post_router.get("/posts")
async def listing(db: AsyncSession = Depends(get_db)):
    return await posts_get_all(db)

@post_router.get("/posts/{id}")
async def detail(id: int, db: AsyncSession = Depends(get_db)):
    return await posts_get_one(id, db)

@post_router.delete("/posts/{id}")
async def detail_delete(id: int, db: AsyncSession = Depends(get_db)):
    return await post_delete(id, db)

@post_router.put("/posts/{id}")
async def detail_update(id: int, body: UpdatePost, db: AsyncSession = Depends(get_db)):
    if body.model_dump(exclude_none=True) == {}:
        raise HTTPException(401, detail="Надо хотя-бы чё-то изменить")
    return await post_update(id, body, db)
