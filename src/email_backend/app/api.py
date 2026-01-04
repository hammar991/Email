"""
主函数
"""
from fastapi import FastAPI
import uvicorn

from src.email_backend.core.config import settings
from src.email_backend.app.api_router import api_router


app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    root_path=settings.API_V1_STR
)


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)