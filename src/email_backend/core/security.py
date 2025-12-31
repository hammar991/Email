"""
安全验证
"""
import secrets
from pwdlib import PasswordHash

# 密码哈希算法
password_hash = PasswordHash.recommended()


def create_access_token():
    """
    创建token访问令牌
    :return:
    """
    pass


def get_current_user(token: str):
    pass



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