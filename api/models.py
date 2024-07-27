from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from db.models import User


class CreateUser(BaseModel):
	username: str = Field(
		min_length=5, max_length=32
	)
	password: str = Field(
		min_length=8, max_length=64
	)
	image: Optional[str] = Field(
		default = 'kfkdgkdngkndkgkdmgkmdkgmdkgmdkm'
	)
	email: EmailStr

	class Config:
		from_attributes = True

class ShowUser(BaseModel):
	id: int
	username: str
	image: str
	email: EmailStr
	is_active: bool

	class Config:
		from_attributes = True


class UpdateUser(BaseModel):
	username: str | None = None
	password: str 
	image: str = Field(
		default = 'kfkdgkdngkndkgkdmgkmdkgmdkgmdkm'
	)
	email: EmailStr

	class Config:
		from_attributes = True

class CreatePost(BaseModel):
	title: str | None = None
	post_image: str | None = None
	content: str
	owner_id: int

	class Config:
		from_attributes = True
		arbitrary_types_allowed = True

class ShowPost(BaseModel):
	id: int
	title: str | None = None
	post_image: str | None = None
	content: str
	owner_id: int

	class Config:
		from_attributes = True
		arbitrary_types_allowed=True

class UpdatePost(BaseModel):
	title: str | None
	post_image: str | None
	content: str | None

	class Config:
		from_attributes = True
