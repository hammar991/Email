"""
序列化层:pydantic模型
"""

from pydantic import BaseModel, EmailStr, model_validator
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime


class RegisterMsg(BaseModel):
    """ 注册请求 """
    name: str
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    """ 注册响应 """
    status_code: int
    name: str
    detail: str


class LoginMsg(BaseModel):
    """ 登录请求 """
    username: str
    password: str


class Token(BaseModel):
    """ token """
    access_token: str
    token_type: str


class UserResetMsg(BaseModel):
    """ 用户重置密码 """
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
    """ 获取用户信息请求 """
    id: int
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    """ 更新用户信息请求 """
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr


class MailboxMsg(BaseModel):
    """ 获取信箱请求 """
    name: str
    title: str | None



class MailboxResponse(BaseModel):
    """ 信箱数据响应 """
    id: int
    box_name: str
    title: str
    share_token: str


class MessageInfo(BaseModel):
    """ 信件信息 """
    headline: str
    context: str
    box_id: int


class MessageResponse(BaseModel):
    """ 信件响应 """
    id: int
    headline: str
    context: str
    box_id: int
    created_at: datetime


class PublicMessageCreate(BaseModel):
    headline: str

    context: Optional[str]


class CredentialResponse(BaseModel, JSONResponse):
    """验证失败响应"""
    status_code: int = 401
    detail: str = "无法验证凭证!"


class SuccessResponse(BaseModel):
    status: int = 200
    detail: str = ""
