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


class MessageInfo(BaseModel):
    context: str
