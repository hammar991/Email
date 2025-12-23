"""
@File: config.py
基本设置
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TITLE :str = "信箱项目"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "0.1.0"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30       # 访问令牌过期时间
    DATABASE_URL: str = "sqlite///C:/Users/user/PycharmProjects/Email/src/email_backend/schemes/__init__.py"         # 数据库


settings = Settings()