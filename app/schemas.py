from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content:  str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    title: Optional[str]
    content: Optional[str]
    id: Optional[int]
    created_at: Optional[datetime]
    #owner_id: Optional[int]
    owner: Optional[UserOut] = None

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    conversation_id: Optional[int]
    title: Optional[str]
    content: Optional[str]
    created_at: Optional[datetime]
    owner: Optional[UserOut] = None
    votes: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    user_id: int
    post_id: int
    dir: conint(ge=0, le=1) # type: ignore

    class Config:
        from_attributes = True
