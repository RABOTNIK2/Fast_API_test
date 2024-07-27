from fastapi import APIRouter, Depends, HTTPException
from .models import ShowUser, CreateUser, UpdateUser
from db.session import get_db
from db.operations import UserView
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

user_router = APIRouter(tags=['UserController'])

async def user_post(body: CreateUser, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_cont = UserView(session)
            user = await user_cont.create(body)
            return ShowUser(
                id=user.id,
                username=user.username,
                image=user.image,
                email=user.email,
                is_active=user.is_active
            )
        
async def user_get_all(db):
    async with db as session:
        async with session.begin():
            user_cont = UserView(session)
            users = await user_cont.user_list()
            return users

async def user_delete(id: int, db):
    async with db as session:
        async with session.begin():
            user_cont = UserView(session)
            return await user_cont.user_detail_delete(id)
        
async def user(id: int, db):
    async with db as session:
        async with session.begin():
            user_cont = UserView(session)
            user = await user_cont.user_detail(id)
            return user

async def user_put(id: int, body: UpdateUser, db):
    async with db as session:
        async with session.begin():
            user_count = UserView(session)
            upd_user = await user_count.user_detail_update(id=id, body=body)
            return upd_user

async def user_patch(id: int, db):
    async with db as session:
        async with session.begin():
            user_count = UserView(session)
            return await user_count.user_ban(id)


@user_router.post("/users", response_model=ShowUser)
async def new_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await user_post(body, db)
    except IntegrityError:
        return HTTPException(503, detail="Email должен быть уникальным")
    
@user_router.get("/users")
async def all_list(db: AsyncSession = Depends(get_db)):
    return await user_get_all(db)

@user_router.delete("/users/{id}")
async def del_user(id: int, db: AsyncSession = Depends(get_db)):
    return await user_delete(id, db)

@user_router.get("/users/{id}")
async def detail_user(id: int, db: AsyncSession = Depends(get_db)):
    return await user(id, db)

@user_router.put("/users/{id}")
async def updated_user(id: int, body: UpdateUser, db: AsyncSession = Depends(get_db)):
    try:
        if body.model_dump(exclude_none=True) == {}:
            raise HTTPException(401, detail="Надо хотя-бы чё-то изменить")
        return await user_put(id, body, db)
    except IntegrityError:
        return HTTPException(503, detail="Данный email уже занят")
    
@user_router.patch("/users/{id}")
async def banned_user(id: int, db: AsyncSession = Depends(get_db)):
    return await user_patch(id, db)