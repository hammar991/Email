"""
邮件接口
"""
from fastapi import APIRouter

from src.email_backend.services.messageService import MessageService

router = APIRouter(
    prefix="/message",
    tags=["邮件接口"]
)

@router.get("")
def get_message(box_id: int):
    """
    获取某邮箱所有邮件
    """
    pass

@router.delete("")
def delete_message():
    """
    删除邮件
    """
    pass

@router.post("/public/mailbox/{share_token}/message")
def submit_message():
    """
    投递信件
    """
    pass


