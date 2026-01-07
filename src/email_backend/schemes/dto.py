"""
序列化层：pydantic模型
"""
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse


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


class UserInfo(BaseModel):
    id: int
    name: str
    email: EmailStr


class MessageInfo(BaseModel):
    context: str


class SuccessfulResponse(BaseModel, JSONResponse):
    status_code: int = 200
    message: str
    code: int
    detail: str


class CredentialResponse(BaseModel, JSONResponse):
    """验证失败响应"""
    status_code: int = 401
    detail:str = "无法验证凭证!"
