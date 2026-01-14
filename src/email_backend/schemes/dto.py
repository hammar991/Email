"""
序列化层：pydantic模型
"""
from dataclasses import field

from pydantic import BaseModel, EmailStr, field_validator, ValidationError,model_validator
from fastapi.responses import JSONResponse
from typing import Optional


class RegisterMsg(BaseModel):
    name: str
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    """注册响应"""
    status_code: int
    name: str
    detail: str


class LoginMsg(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResetMsg(BaseModel):
    name: str
    email: EmailStr
    password: str
    ensure_password: str

    # 验证：密码 == 确认密码
    @model_validator(mode="after")
    def check_password_match(self):
        pw1 = self.password
        pw2 = self.ensure_password
        if not pw1 or not pw2 or pw1 != pw2:
            raise ValueError("密码和确认密码不一致！")
        return self


class UserInfo(BaseModel):
    id: int
    name: str
    email: EmailStr


class MailboxMsg(BaseModel):
    name: EmailStr
    user_id: int

class ResMailboxMsg(BaseModel):
    id : int
    name : EmailStr

class MessageInfo(BaseModel):
    context: str


class CredentialResponse(BaseModel, JSONResponse):
    """验证失败响应"""
    status_code: int = 401
    detail:str = "无法验证凭证!"
