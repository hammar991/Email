"""
邮箱接口
"""

from fastapi import APIRouter, Depends
from loguru import logger
from sqlmodel import Session

from src.email_backend.services.mailboxService import MailboxService
from src.email_backend.services.userService import UserServices
from src.email_backend.core.databases import get_db_session
from src.email_backend.schemes.entity import User
from src.email_backend.core.security import get_current_user_name
from src.email_backend.schemes.dto import ResMailboxMsg

router = APIRouter(
    prefix="/box",
    tags=["邮箱接口"]
)


@router.get("/mailbox")
def get_mailbox(current_user_name: str = Depends(get_current_user_name)):
    """
    拿到当前用户所有的邮箱
    :param current_user_name:
    :return:
    """
    with get_db_session() as session:
        logger.debug(current_user_name)
        mailbox_service = MailboxService(session=session)
        user_server = UserServices(session=session)
        user = user_server.get_user_by_name(current_user_name)
        logger.debug(user)
        resp: ResMailboxMsg = mailbox_service.get_mailbox_by_user_id(user.id)
        logger.debug('111', resp)
        return {"result": resp}


@router.post("/create_mailbox")
def create_mailbox():
    """
    创建邮箱
    """


# @router.post("/mailbox")
# def modify_mailbox():
#     pass

@router.delete("/mailbox")
def get_mailbox():
    pass


@router.get("/share_mailbox")
def share_mailbox():
    pass
