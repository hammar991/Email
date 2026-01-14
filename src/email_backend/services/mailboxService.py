"""
邮箱crud
"""
from fastapi import HTTPException
from sqlmodel import select
from starlette import status
from loguru import logger

from src.email_backend.schemes.entity import Mailbox
from src.email_backend.schemes.dto import MailboxMsg, ResMailboxMsg
from src.email_backend.services.serviceBase import ServiceBase


class MailboxService(ServiceBase):

    def create_mailbox(self, mailbox: MailboxMsg):
        """创建邮箱"""
        statement = Mailbox(box_name=mailbox.name, user_id=mailbox.user_id)
        self._s.add(statement)
        return True

    def delete_mailbox(self, mailbox: MailboxMsg):
        """删除邮箱"""
        statement = select(Mailbox).where(Mailbox.box_name == mailbox.name and Mailbox.user_id == mailbox.user_id)
        resp = self._s.exec(statement).one()
        if not resp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到邮箱！"
            )
        self._s.delete(resp)
        return True

    # def update_mailbox(self, mailbox):
    #     """更新邮箱信息"""
    #     pass

    def get_mailbox_by_user_id(self, uid: int):
        """
        拿到用户下所有邮箱
        :param uid:
        :return:
        """
        statement = select(Mailbox).where(Mailbox.user_id == uid)
        resp = self._s.exec(statement).all()
        logger.debug(resp)
        logger.debug(type(resp))
        return [ResMailboxMsg.model_validate(m) for m in resp]
