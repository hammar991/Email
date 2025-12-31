"""
登录接口
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from src.email_backend.core.config import settings

router = APIRouter(
    prefix="/user",
    tags=["登录注册接口"]
)


# 查找包含Bearer令牌的Authorization头(www-Authorization 响应头); 未找到返回 401 error
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/user/login/access-token")

@router.post("/login/access-token")
async def login(
        request: Request,
        form_data: Annotated[OAuth2PasswordRequestForm,Depends()],

):
    pass


@router.post("/register")
def register_user():
    pass