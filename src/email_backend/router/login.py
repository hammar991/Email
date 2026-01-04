"""
登录接口
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)
from typing import Annotated

from src.email_backend.core.config import settings
from src.email_backend.core.security import verify_password, create_access_token
from src.email_backend.schemes.dto import Token
from src.email_backend.services.userService import UserServices
from src.email_backend.core.databases import get_db_session

router = APIRouter(
    prefix="/user",
    tags=["登录注册接口"]
)

# 查找包含Bearer令牌的Authorization头(www-Authorization 响应头); 未找到返回 401 error
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/user/login/access-token")


@router.post("/login/access-token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """登录"""
    with get_db_session() as session:
        user = UserServices.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=404, detail="error！该用户不存在！")

    res = verify_password(form_data.password, user.password)
    if not res:
        raise HTTPException(status_code=401, detail="error！密码错误！")

    access_token = create_access_token(data={"sub": user.name}, expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
def register_user():
    pass
