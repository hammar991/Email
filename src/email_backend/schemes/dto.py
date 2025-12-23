"""
序列化层：pydantic模型
"""
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class MessageInfo(BaseModel):
    context: str
