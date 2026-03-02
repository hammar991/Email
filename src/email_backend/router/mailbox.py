"""
信箱接口
"""
from fastapi import APIRouter
from loguru import logger
from typing import List

from src.email_backend.services.mailboxService import MailboxService
from src.email_backend.core.databases import DBSessionDependency
from src.email_backend.schemes.dto import MailboxMsg, MailboxResponse
from src.email_backend.core.security import AuthDependency

router = APIRouter(
    prefix="/box",
    tags=["信箱接口"]
)


@router.get("/mailbox/{box_name}", response_model=MailboxResponse)
def get_mailbox(box_name: str, user: AuthDependency, session: DBSessionDependency):
    """
    获取某一信箱
    """
    mailbox_service = MailboxService(session=session)
    return mailbox_service.get_mailbox_by_name(box_name,user.id)



@router.get("/mailbox", response_model=List[MailboxResponse])
def get_mailbox(user: AuthDependency, session: DBSessionDependency):
    """
    拿到当前用户所有的信箱
    """
    mailbox_service = MailboxService(session=session)
    logger.debug('2222',mailbox_service)
    return mailbox_service.get_mailbox_by_user_id(user.id)


@router.post("/mailbox", response_model=MailboxResponse)
def create_mailbox(box_name: str, title: str, user: AuthDependency, session: DBSessionDependency):
    """
    创建信箱
    """
    mailbox_service = MailboxService(session=session)
    entity = MailboxMsg(
        name= box_name,
        title=title,
        user_id=user.id,
    )
    return mailbox_service.create_mailbox(entity)


@router.delete("/mailbox",response_model=MailboxResponse)
def get_mailbox(box_id: int,  user: AuthDependency,session: DBSessionDependency):
    """
    删除信箱
    """
    mailbox_service = MailboxService(session=session)
    return mailbox_service.delete_mailbox_by_id(box_id, user.id)

"""无需登录"""
@router.get("/share_mailbox/{share_token}", response_model=MailboxResponse)
def get_public_mailbox(share_token: str, session: DBSessionDependency):
    """
    公开分享信箱
    """
    logger.debug('2222',share_token)
    mailbox_service = MailboxService(session=session)
    mailbox = mailbox_service.get_mailbox_by_share_token(share_token)
    logger.debug('11',mailbox)
    return mailbox