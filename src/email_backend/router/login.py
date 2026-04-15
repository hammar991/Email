"""
登录接口
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from src.email_backend.core.config import SETTINGS
from src.email_backend.core.databases import DBSessionDependency
from src.email_backend.core.security import create_access_token
from src.email_backend.schemes.dto import Token, RegisterMsg, RegisterResponse, UserResetMsg, SuccessResponse
from src.email_backend.services.userService import UserServices

router = APIRouter(
    tags=["登录注册接口"]
)


@logger.catch()
@router.post("/login/access-token")
async def login(session: DBSessionDependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """登录"""
    print(form_data.username)
    print(form_data.password)
    user_service = UserServices(session=session)
    res = user_service.authenticate_user(form_data.username, form_data.password)

    if not res:
        raise HTTPException(status_code=401, detail="error！密码错误！")
    user = user_service.get_user_by_name(form_data.username)
    access_token = create_access_token(data={"sub": user.name}, expires_delta=SETTINGS.access_token_expire_minutes)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
def register_user(user_data: RegisterMsg, session: DBSessionDependency):
    """注册"""
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
def reset_password(form_data: UserResetMsg, session: DBSessionDependency):
    """
    重置密码
    :param form_data:
    :return:
    """
    user_service = UserServices(session=session)
    resp = user_service.reset_password(data=form_data)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail="更新数据失败！请再试一次!"
        )

    return SuccessResponse(
        detail="更新成功"
    )
