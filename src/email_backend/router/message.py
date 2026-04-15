"""
信件接口
"""
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from typing import List

from services.messageService import MessageService
from core.databases import DBSessionDependency
from core.security import AuthDependency
from schemes.dto import PublicMessageCreate, MessageInfo,MessageResponse

router = APIRouter(
    prefix="/message",
    tags=["信件接口"]
)


@router.get("/mail", response_model=List[MessageResponse])
def get_message(box_id: int, user: AuthDependency, session: DBSessionDependency):
    """
    获取某信箱所有信件
    """
    if user:
        message_service = MessageService(session=session)
        return message_service.get_mail_by_box_id(box_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_UNAUTHORIZED,
            detail="请登录再操作！"
        )


@router.delete("/mail", response_model=MessageResponse)
def delete_message(message_id: int, box_id: int, user: AuthDependency, session: DBSessionDependency):
    """
    删除信件
    """
    if user:
        message_service = MessageService(session=session)
        return message_service.delete_mail(message_id, box_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_UNAUTHORIZED,
            detail="请登录再操作！"
        )


@router.post("/mail",response_model=MessageResponse)
def create_message(message_data: MessageInfo, user: AuthDependency, session: DBSessionDependency):
    """
    创建信件
    """
    if user:
        message_service = MessageService(session=session)
        return message_service.create_mail(message_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_UNAUTHORIZED,
            detail="请登录再操作！"
        )


@router.post("/public/mailbox/{share_token}/message",response_model=MessageResponse)
def submit_message(share_token: str, message_data: PublicMessageCreate, session: DBSessionDependency):
    """
    投递信件（无需登录，匿名投递）
    """
    message_service = MessageService(session=session)
    return message_service.submit_mail_by_share_token(
        share_token, message_data.headline, message_data.context
    )


