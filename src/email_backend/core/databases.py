"""
数据库连接
"""
from sqlmodel import create_engine, Session
from fastapi import Depends
from loguru import logger
from typing import Annotated

from src.email_backend.core.config import SETTINGS

# 创建数据库引擎
engine = create_engine(url=SETTINGS.database_url, echo=False, pool_size=SETTINGS.pool_size,
                       max_overflow=SETTINGS.max_overflow)
logger.info(f'创建数据库引擎：{engine}')


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

        except Exception as e:  # 发生异常,回滚事务  重新抛出异常
            logger.exception(e)
            session.rollback()
            raise
        finally:  # 无论是否异常 , 都会记录
            logger.trace("db session closed!")
            session.close()


DBSessionDependency: type[Session] = Annotated[Session, Depends(get_db_session)]
