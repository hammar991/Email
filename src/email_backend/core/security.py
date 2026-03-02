"""
安全验证
"""
from datetime import timedelta, datetime, timezone
from typing import Annotated

import jose
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from sqlmodel import Session

from src.email_backend.core.config import SETTINGS
from src.email_backend.schemes.dto import CredentialResponse
from src.email_backend.schemes.entity import User
from src.email_backend.services.userService import UserServices
from src.email_backend.core.databases import get_db_session


# 查找包含Bearer令牌的Authorization头(www-Authorization 响应头); 未找到返回 401 error
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{SETTINGS.api_v1_str}/login/access-token")


def create_access_token(data: dict, expires_delta: int | None = None):
    """
    创建token访问令牌
    :param data: 包含用户信息字典
    :param expires_delta: 过期时间
    :return: 编码后的jwt字符串
    """
    # 1.复制一份，避免修改原始传入的数据
    to_encode = data.copy()

    # 2. 设置过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    # 3. 添加过期时间
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SETTINGS.secret_key, algorithm=SETTINGS.algorithm)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session:Session = Depends(get_db_session)):
    """
    拿到当前用户
    :return:
    """
    try:
        payload = jwt.decode(token, SETTINGS.secret_key, algorithms=SETTINGS.algorithm)
        username: str = payload.get("sub")
        logger.debug(f"username:{username}")
        if username is None:
            raise CredentialResponse
        user_service = UserServices(session)
        user = user_service.get_user_by_name(username)
        return user
    except jose.JWTError:
        raise CredentialResponse

AuthDependency : type[User] = Annotated[User, Depends(get_current_user)]
