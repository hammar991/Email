"""
邮箱接口
"""

from fastapi import APIRouter, Depends
from loguru import logger
from pydantic import EmailStr
from sqlmodel import Session

from src.email_backend.services.mailboxService import MailboxService
from src.email_backend.services.userService import UserServices
from src.email_backend.core.databases import get_db_session
from src.email_backend.schemes.dto import MailboxMsg
from src.email_backend.core.security import get_current_user_name

router = APIRouter(
    prefix="/box",
    tags=["邮箱接口"]
)


@router.get("/mailbox/{box_name}")
def get_mailbox(box_name: str, name : str):
    """
    获取某一邮箱
    """
    with get_db_session() as session:
        mailbox_service = MailboxService(session=session)
        user_server = UserServices(session=session)
        user = user_server.get_user_by_name(name)
        return mailbox_service.get_mailbox_by_name(box_name,user.id).model_dump(mode="json", exclude={"user_id"})



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
        return [i.model_dump(mode="json", exclude={"user_id"}, ) for i in
                mailbox_service.get_mailbox_by_user_id(user.id)]


@router.post("/create_mailbox")
def create_mailbox(box_name: EmailStr, current_user_name: str = Depends(get_current_user_name)):
    """
    创建邮箱
    """
    with get_db_session() as session:
        mailbox_service = MailboxService(session=session)
        user_server = UserServices(session=session)
        entity = MailboxMsg(
            name= box_name,
            user_id=user_server.get_user_by_name(current_user_name).id,
        )
        return mailbox_service.create_mailbox(entity).model_dump(mode="json", exclude={"user_id", "id"})


@router.delete("/mailbox")
def get_mailbox(box_id: int,  current_user_name: str = Depends(get_current_user_name)):
    """
    删除邮箱
    """
    with get_db_session() as session:
        mailbox_service = MailboxService(session=session)
        user_server = UserServices(session=session)
        user = user_server.get_user_by_name(current_user_name)
        return mailbox_service.delete_mailbox_by_id(box_id, user.id).model_dump(mode="json")

"""无需登录"""
@router.get("/share_mailbox/{share_token}")
def get_public_mailbox(share_token: str):
    """
    公开分享信箱
    """
    logger.debug('2222',share_token)
    with get_db_session() as session:
        mailbox_service = MailboxService(session=session)
        mailbox = mailbox_service.get_mailbox_by_share_token(share_token)
        logger.debug('11',mailbox)
        return mailbox.model_dump(mode="json", exclude={"user_id"})