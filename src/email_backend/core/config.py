"""
@File: config.py
配置文件
"""
import os
from pydantic_settings import BaseSettings
from loguru import logger
from pathlib import Path

class Settings(BaseSettings):
    # 项目基本信息
    title :str = "信箱项目2.0"
    api_v1_str: str = "/api/v1"
    version: str = "0.1.0"
    project_name: str = "信箱系统"
    description: str = "这是一个信箱系统，支持用户使用多个信箱进行收发邮件及分享邮箱，技术栈:FastAPI + SQLModel + Sqlite"

    # jwt访问令牌
    access_token_expire_minutes: int = 180       # 访问令牌过期时间
    algorithm: str = "HS256"  # 算法
    secret_key: str = ''

    # 数据库
    database_url: str = f"sqlite:///{os.path.join(os.path.dirname(__file__), '../schemes/database.db')}"
    pool_size: int =  256       # 连接池中保持打开的连接数量
    max_overflow: int = 0       # 设置连接池允许超出 pool_size 限制的最大连接数

    # 静态资源目录
    static_dir: str = os.path.join(os.getcwd(), "../static")

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent.parent / ".env"      # __file__ 本文件  resolve()获取绝对路径

try:
    SETTINGS = Settings()
except Exception as e:
    logger.exception(e)
    exit()