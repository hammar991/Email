"""
主函数
"""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.email_backend.app.api_router import api_router
from src.email_backend.core.config import SETTINGS
from src.email_backend.core.databases import engine
from src.email_backend.schemes.entity import init_db


@asynccontextmanager
async def lifespan(app1 : FastAPI):
    # -- 启动 --
    logger.info(f"正在连接数据库：{SETTINGS.database_url}")

    # 初始化数据库
    init_db(engine)
    logger.info("数据可初始化完成！")
    yield

    # -- 关闭 --
    logger.info("应用关闭，已释放资源...")


app = FastAPI(
    name=SETTINGS.project_name,
    title=SETTINGS.title,
    version=SETTINGS.version,
    root_path=SETTINGS.api_v1_str,
    description=SETTINGS.description,
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # 允许前端域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003)
