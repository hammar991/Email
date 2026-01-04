"""
序列化层：pydantic模型
"""
from pydantic import BaseModel, EmailStr


class RegisterMsg(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginMsg(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class UserInfo(BaseModel):
    id: int
    name: str
    email: EmailStr


class MessageInfo(BaseModel):
    context: str
