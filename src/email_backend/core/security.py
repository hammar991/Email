"""
安全验证
"""
import secrets
from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone

import jwt

from src.email_backend.core.config import settings

# 密码哈希算法
password_hash = PasswordHash.recommended()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
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
        expire = datetime.now(timezone.utc) + expires_delta
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


def verify_password(plain_password, hashed_password):
    """
    验证密码是否匹配
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return password_hash.verify(plain_password, hashed_password)


def get_secret_key():
    """
    返回十六进制字符串
    :return:
    """
    return secrets.token_hex(32)


if __name__ == "__main__":
    a = get_secret_key()
    print(a)