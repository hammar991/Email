"""
信箱crud
"""
from fastapi import HTTPException
from sqlmodel import select
from starlette import status
from loguru import logger
from typing import Iterable

from schemes.entity import Mailbox
from schemes.dto import MailboxMsg
from services.serviceBase import ServiceBase


class MailboxService(ServiceBase):

    def create_mailbox(self, mailbox: MailboxMsg, user_id: int):
        """创建信箱"""
        entity = Mailbox(box_name=mailbox.name, title=mailbox.title, user_id=user_id)
        self._s.add(entity)
        return entity

    def delete_mailbox_by_id(self, mailbox_id: int, user_id: int):
        """删除信箱"""
        statement = select(Mailbox).where(Mailbox.id == mailbox_id and Mailbox.user_id == user_id)
        resp = self._s.exec(statement).one()
        if not resp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到信箱！"
            )
        self._s.delete(resp)
        return resp

    def get_mailbox_by_user_id(self, uid: int):
        """
        拿到用户下所有信箱
        :param uid:
        :return:
        """
        statement = select(Mailbox).where(Mailbox.user_id == uid)
        resp: Iterable[Mailbox] | None = self._s.exec(statement).all()
        logger.debug(resp)
        logger.debug(type(resp))
        yield from resp

    def get_mailbox_by_name(self, name: str, user_id: int):
        """
        根据信箱名查取信箱
        :param name:
        :param user_id:
        :return:
        """
        statement = select(Mailbox).where(Mailbox.box_name == name and Mailbox.user_id == user_id)
        resp = self._s.exec(statement).one()
        if not resp:
            return None
        return resp

    def get_mailbox_by_share_token(self, share_token: str):
        """
        :param share_token:
        :param share_token:
        :return:
        """
        statement = select(Mailbox).where(Mailbox.share_token == share_token)
        resp = self._s.exec(statement).one()
        logger.debug(resp)
        if not resp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到信箱！"
            )
        return resp
