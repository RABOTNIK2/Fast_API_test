from .models import User, Posts
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, update, select, delete
from fastapi import HTTPException
from api.models import CreateUser, UpdateUser, CreatePost, UpdatePost
from fastapi.responses import JSONResponse

class UserView:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def user_list(self):
        query = select(User)
        result = await self.db_session.execute(query)
        users = result.scalars().all()
        return users

    async def create(self, body: CreateUser) -> User:
        new_user = User(
            username = body.username,
            password = body.password,
            image = body.image,
            email = body.email
        )
        self.db_session.add(new_user)
        await self.db_session.commit()
        return new_user
    
    async def user_detail(self, id: int):
        query = select(User).where(User.id == id)
        result = await self.db_session.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                404, detail="Пользователь не найден"
            )
        return user
    
    async def user_detail_delete(self, id: int):
        query = select(User).where(User.id == id)
        results = await self.db_session.execute(query)
        dell = results.scalars().first()
        if not dell:
            raise HTTPException(
                404, detail="Пользователь не найден"
            )
        deleted_user = delete(User).where(User.id == id)
        results = await self.db_session.execute(deleted_user)
        return JSONResponse(content={'message': 'Пользователь удалён'})
    
    async def user_detail_update(self, body: UpdateUser, id: int):
        query = select(User).where(and_(User.id == id, User.is_active == True))
        results = await self.db_session.execute(query)
        user = results.scalars().first()
        if not user:
            raise HTTPException(
                404, detail="Пользователь не найден"
            )
        updated_query = update(User).where(and_(User.id==id, User.is_active==True)).values(**body.model_dump(exclude_none=True))
        results = await self.db_session.execute(updated_query)

        return user

    async def user_ban(self, id: int):
        query = select(User).where(User.id==id, User.is_active==True)
        results = await self.db_session.execute(query)
        user = results.scalars().first()
        if not user:
            raise HTTPException(
                404, detail="Пользователь не найден или забанен"
            )
        new_query = update(User).where(User.id==id, User.is_active==True).values(is_active=False)
        results = await self.db_session.execute(new_query)

        return JSONResponse(content={'message': 'Пользователь забанен'})

class PostController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def post_list(self):
        query = select(Posts)
        results = await self.db_session.execute(query)
        posts = results.scalars().all()
        return posts

    async def create(self, body: CreatePost) -> Posts:
        query = select(User).where(User.id==body.owner_id, User.is_active==True)
        results = await self.db_session.execute(query)
        user = results.scalars().first()
        if not user:
            raise HTTPException(
                404, detail="Чего?"
            )
        new_post = Posts(
            title=body.title,
            post_image=body.post_image,
            content=body.content,
            owner_id=body.owner_id,
            owner=user
        )
        self.db_session.add(new_post)
        await self.db_session.commit()
        return new_post
    
    async def post_detail(self, id: int):
        query = select(Posts).where(Posts.id == id)
        results = await self.db_session.execute(query)
        post = results.scalars().first()
        if not post:
            raise HTTPException(
                404, detail="Поста не существует"
            )
        return post
    
    async def post_detail_delete(self, id: int):
        query = select(Posts).where(Posts.id == id)
        results = await self.db_session.execute(query)
        post = results.scalars().first()
        if not post:
            raise HTTPException(
                404, detail="Поста не существует"
            )
        del_post = delete(Posts).where(Posts.id == id)
        results = await self.db_session.execute(del_post)
        return JSONResponse(content={"message": "Пост удалён"})

    async def post_detail_update(self, id: int, body: UpdatePost):
        query = select(Posts).where(Posts.id == id)
        results = await self.db_session.execute(query)
        post = results.scalars().first()
        if not post:
            raise HTTPException(
                404, detail="Поста не существует"
            )
        upd_query = update(Posts).where(Posts.id == id).values(**body.model_dump(exclude_none=True))
        results = await self.db_session.execute(upd_query)
        return post
