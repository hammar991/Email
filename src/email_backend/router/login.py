"""
登录接口
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from src.email_backend.core.config import settings
from src.email_backend.core.databases import get_db_session
from src.email_backend.core.security import verify_password, create_access_token
from src.email_backend.schemes.dto import Token, RegisterMsg, RegisterResponse
from src.email_backend.services.userService import UserServices

router = APIRouter(
    prefix="/user",
    tags=["登录注册接口"]
)


@logger.catch()
@router.post("/login/access-token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """登录"""
    with get_db_session() as session:
        user_service = UserServices(session=session)
        user = user_service.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="error！该用户不存在！",
                headers={"WWW-Authenticate": "Bearer"},
            )
        res = verify_password(form_data.password, user.password)
        if not res:
            raise HTTPException(status_code=401, detail="error！密码错误！")

        access_token = create_access_token(data={"sub": user.name}, expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
def register_user(user_data: RegisterMsg):
    """注册"""
    with get_db_session() as session:
        user_service = UserServices(session=session)
        logger.debug(user_data)
        # 创建用户
        res = user_service.create_user(data=user_data)
        logger.debug(res)

        if not res:
            raise HTTPException(
                status_code=404,
                detail="创建失败！！"
            )

        return RegisterResponse(
            name=user_data.name,
            status_code=200,
            detail="创建成功！"
        )


@router.post("/login/reset")
def reset_password(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    重置密码
    :param form_data:
    :return:
    """
    with get_db_session() as session:
        user_service = UserServices(session=session)


