"""
主函数
"""
from fastapi import FastAPI
import uvicorn

from src.email_backend.config.config import settings


app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)