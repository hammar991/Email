"""
@File: config.py
配置文件
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 项目基本信息
    TITLE :str = "信箱项目2.0"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "信箱系统"
    DESCRIPTION: str = "这是一个信箱系统，支持用户使用多个信箱进行收发邮件及分享邮箱，技术栈:FastAPI + SQLModel + Sqlite"

    # jwt访问令牌
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30       # 访问令牌过期时间
    ALGORITHM: str = "HS256"  # 算法
    SECRET_KEY: str = "56f060e77af06f79b96dec1f5c4332cdc803b181354c4a40060502b7bc589fc4"

    # 数据库
    DATABASE_URL: str = "sqlite:///C:/Users/user/Desktop/email/src/email_backend/schemes/database.db"

    # 静态资源目录
    STATIC_DIR: str = os.path.join(os.getcwd(), "../static")


settings = Settings()