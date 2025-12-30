"""
数据库连接
"""
from sqlmodel import create_engine,Session
from loguru import logger
from contextlib import contextmanager

from src.email_backend.core.config import settings
from src.email_backend.schemes.entity import init_db


# 创建数据库引擎
engine = create_engine(url=settings.DATABASE_URL, echo=True)

# 数据库初始化
init_db(engine)

"""上下文管理器"""
@contextmanager
def get_db_session():
    with Session(engine) as session:
        try:
            logger.trace(f"db session start!")
            yield session

            # with 块执行完毕后回到这里
            logger.trace("db session end!")

            # 无异常,提交事务
            session.commit()
            logger.trace("db session commit!")

        except Exception as e:      # 发生异常,回滚事务  重新抛出异常
            logger.exception(e)
            session.rollback()
            raise
        finally:        # 无论是否异常 , 都会记录
            logger.trace("db session closed!")
