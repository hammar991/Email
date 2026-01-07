"""
邮箱接口
"""

from fastapi import APIRouter, Depends

from src.email_backend.services.mailboxService import MailboxService
from src.email_backend.services.userService import UserServices
from src.email_backend.core.databases import get_db_session
from src.email_backend.schemes.entity import User
from src.email_backend.core.security import get_current_user

router = APIRouter(
    prefix = "/box",
    tags=["邮箱接口"]
)


@router.get("/mailbox")
def get_mailbox(current_user: User = Depends(get_current_user)):
    """
    拿到当前用户所有的邮箱
    :param current_user:
    :return:
    """
    with get_db_session() as session:
        mailbox_service = MailboxService(session)
        resp = mailbox_service.get_mailbox_by_user_id(current_user.id)
        print(resp)


@router.post("/create_mailbox")
def create_mailbox():
    pass

@router.post("/mailbox")
def modify_mailbox():
    pass

@router.delete("/mailbox")
def get_mailbox():
    pass

@router.get("/share_mailbox")
def share_mailbox():
    pass