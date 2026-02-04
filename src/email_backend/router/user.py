"""
用户接口
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from src.email_backend.core.databases import get_db_session
from src.email_backend.core.security import get_current_user_name
from src.email_backend.services.userService import UserServices
from src.email_backend.schemes.dto import UserInfo,UserUpdate

router = APIRouter(
    prefix="/user",
    tags=["用户接口"]
)


@router.get("/userinfo")
def get_user(current_user_name: str = Depends(get_current_user_name)):
    """
    获取当前用户信息
    """
    with get_db_session() as session:
        user_service = UserServices(session=session)
        user = user_service.get_user_by_name(current_user_name)
        return user.model_dump(mode="json")


@router.put("/userinfo")
def update_user(user_data: UserUpdate, current_user_name: str = Depends(get_current_user_name)):
    """
    更新用户信息
    """
    with get_db_session() as session:
        user_service = UserServices(session=session)
        user = user_service.get_user_by_name(current_user_name)
        user.email = user_data.email
        session.add(user)
        return user.model_dump(mode="json")
