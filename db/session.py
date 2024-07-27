from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from settings import DATABASE_URL
from sqlalchemy.orm import sessionmaker
from typing import Generator

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

async def get_db() -> Generator:
	try:
		session: AsyncSession = async_session()
		yield session
	finally:
		await session.close()