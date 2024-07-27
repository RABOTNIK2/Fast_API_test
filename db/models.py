from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, Column, Integer
from sqlalchemy import ForeignKey

class Base(DeclarativeBase): pass

class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	username: Mapped[str] = mapped_column(String(30))
	password: Mapped[str] = mapped_column(String(32))
	image: Mapped[str] = mapped_column(default='kfkdgkdngkndkgkdmgkmdkgmdkgmdkm')
	email: Mapped[str] = mapped_column(unique=True)
	is_active: Mapped[bool] = mapped_column(default=True) 

class Posts(Base):
	__tablename__ = "posts"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	title: Mapped[str] = mapped_column(String(100))
	post_image: Mapped[str] = mapped_column(nullable=True)
	content: Mapped[str] = mapped_column(nullable=False)
	owner_id = Column(Integer, ForeignKey("users.id"))
	
	owner = relationship("User")


	