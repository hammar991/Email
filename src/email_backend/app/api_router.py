"""
路由聚合
"""

from fastapi import APIRouter

from router import login,message,user,mailbox

api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(message.router)
api_router.include_router(user.router)
api_router.include_router(mailbox.router)