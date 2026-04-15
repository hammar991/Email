"""
用户接口
"""

from fastapi import APIRouter

from src.email_backend.core.databases import DBSessionDependency
from src.email_backend.core.security import AuthDependency
from src.email_backend.schemes.dto import UserUpdate, UserResponse

router = APIRouter(
    prefix="/user",
    tags=["用户接口"]
)


@router.get("/userinfo", response_model=UserResponse)
def get_user(user: AuthDependency):
    """
    获取当前用户信息
    """
    return user


@router.put("/userinfo", response_model=UserResponse)
def update_user(user_data: UserUpdate, user: AuthDependency, session: DBSessionDependency):
    """
    更新用户信息
    """
    user.email = user_data.email
    session.add(user)
    return user
