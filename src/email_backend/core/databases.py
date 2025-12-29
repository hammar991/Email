"""
数据库连接
"""
from sqlmodel import create_engine,Session
from loguru import logger

from src.email_backend.core.config import settings
from src.email_backend.schemes.entity import init_db


# 创建数据库引擎
engine = create_engine(url=settings.DATABASE_URL, echo=True)

# 数据库初始化
init_db(engine)

def get_db_session():
    with Session as session:
        try:
            logger.trace(f"db session start!")
            yield session
        except Exception as e:
            logger.exception(e)
            session.rollback()
            raise
