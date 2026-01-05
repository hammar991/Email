"""
主函数
"""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from src.email_backend.app.api_router import api_router
from src.email_backend.core.config import settings
from src.email_backend.core.databases import engine
from src.email_backend.schemes.entity import init_db


@asynccontextmanager
async def lifespan(app1 : FastAPI):
    # -- 启动 --
    logger.info(f"正在连接数据库：{settings.DATABASE_URL}")

    # 初始化数据库
    init_db(engine)
    logger.info("数据可初始化完成！")
    yield

    # -- 关闭 --
    logger.info("应用关闭，已释放资源...")


app = FastAPI(
    name=settings.PROJECT_NAME,
    title=settings.TITLE,
    version=settings.VERSION,
    root_path=settings.API_V1_STR,
    description=settings.DESCRIPTION,
    lifespan=lifespan
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
