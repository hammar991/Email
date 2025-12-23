"""
@File: config.py
基本设置
"""
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    TITLE :str = "信箱项目"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "0.1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30       # 访问令牌过期时间
    SECRET_KEY: str
    DATABASE_URL: str = "sqlite///"         # 数据库
