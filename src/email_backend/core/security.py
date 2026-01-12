"""
安全验证
"""
import secrets
from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select, Session
from typing import Annotated


import jwt, jose
from loguru import logger

from src.email_backend.core.config import settings
from src.email_backend.schemes.entity import User
from src.email_backend.schemes.dto import CredentialResponse
from src.email_backend.core.databases import get_db_session

# 密码哈希算法
password_hash = PasswordHash.recommended()

# 查找包含Bearer令牌的Authorization头(www-Authorization 响应头); 未找到返回 401 error
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/user/login/access-token")

SessionDep = Annotated[Session, Depends(get_db_session)]


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

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str):
    """
    加密密码
    :param password:
    :return:
    """
    return password_hash.hash(password)

@logger.catch()
def verify_password(plain_password, hashed_password):
    """
    验证密码是否匹配
    :param plain_password:
    :param hashed_password:
    :return:
    """
    logger.debug(f"plain_password:{plain_password}, hashed_password: {hashed_password}")
    return password_hash.verify(plain_password, hashed_password)


def get_secret_key():
    """
    返回十六进制字符串
    :return:
    """
    return secrets.token_hex(32)


def get_current_user(session : SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    """
    拿到当前用户
    :return:
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algoriyhms=settings.ALGORITHM)
        username: str = payload.get("sub")
        logger.debug(f"username:{username}")
        if username is None:
            raise CredentialResponse
    except jose.JWTError:
        raise CredentialResponse

    # 验证用户是否存在
    user = session.get(User, username)
    if not user:
        raise CredentialResponse
    return user


if __name__ == "__main__":
    a = get_secret_key()
    print(a)