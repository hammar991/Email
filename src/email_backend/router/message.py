"""
邮件接口
"""
from fastapi import APIRouter

from src.email_backend.services.messageService import MessageService

router = APIRouter(
    prefix="/message",
    tags=["邮件接口"]
)

@router.get("/show")
def get_message(box_id: int):
    """
    获取某邮箱所有邮件
    """



@router.post("/send")
def send_message():
    """
    发送邮件
    """
    pass

@router.post("/message")
def modify_message():
    pass

@router.delete("/message")
def delete_message():
    """
    删除邮件
    """
    pass


