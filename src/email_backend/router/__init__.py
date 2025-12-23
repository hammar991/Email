"""
接口层
"""

from fastapi import APIRouter

from src.email_backend.router.login import router
from src.email_backend.router.mailbox import router
from src.email_backend.router.message import router
from src.email_backend.router.user import router

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(message.router, tags=["messages"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(mailbox.router, tags=["mailbox"])
