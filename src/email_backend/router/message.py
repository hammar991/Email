"""
信件接口
"""
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from typing import List

from src.email_backend.services.messageService import MessageService
from src.email_backend.services.userService import UserServices
from src.email_backend.core.databases import get_db_session
from src.email_backend.core.security import get_current_user_name
from src.email_backend.schemes.dto import PublicMessageCreate, MessageInfo,MessageResponse

router = APIRouter(
    prefix="/message",
    tags=["信件接口"]
)


@router.get("/mail", response_model=List[MessageResponse])
def get_message(box_id: int, current_user_name: str = Depends(get_current_user_name)):
    """
    获取某信箱所有信件
    """
    with get_db_session() as session:
        if current_user_name:
            message_service = MessageService(session=session)
            return message_service.get_mail_by_box_id(box_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_UNAUTHORIZED,
                detail="请登录再操作！"
            )


@router.delete("/mail", response_model=MessageResponse)
def delete_message(message_id: int, box_id: int, current_user_name: str = Depends(get_current_user_name)):
    """
    删除信件
    """
    with get_db_session() as session:
        if current_user_name:
            message_service = MessageService(session=session)
            return message_service.delete_mail(message_id, box_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_UNAUTHORIZED,
                detail="请登录再操作！"
            )


@router.post("/mail",response_model=MessageResponse)
def create_message(message_data: MessageInfo, current_user_name: str = Depends(get_current_user_name)):
    """
    创建信件
    """
    with get_db_session() as session:
        if current_user_name:
            message_service = MessageService(session=session)
            return message_service.create_mail(message_data)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_UNAUTHORIZED,
                detail="请登录再操作！"
            )


@router.post("/public/mailbox/{share_token}/message",response_model=MessageResponse)
def submit_message(share_token: str, message_data: PublicMessageCreate):
    """
    投递信件（无需登录，匿名投递）
    """
    with get_db_session() as session:
        message_service = MessageService(session=session)
        return message_service.submit_mail_by_share_token(
            share_token, message_data.headline, message_data.context
        )


