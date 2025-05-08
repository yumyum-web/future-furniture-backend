from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    username: str
    name: str
    role: Literal["designer", "customer"] = "customer"

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: Optional[str] = None
    password_hash: str

class User(UserBase):
    id: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None