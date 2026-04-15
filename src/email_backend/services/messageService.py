"""
信件crud
"""
from fastapi import HTTPException
from sqlmodel import select
from starlette import status
from typing import Iterable

from schemes.entity import Message, Mailbox
from schemes.dto import MessageInfo
from services.serviceBase import ServiceBase


class MessageService(ServiceBase):

    def create_mail(self, message_info: MessageInfo):
        """
        创建信件
        """
        entity = Message(
            headline=message_info.headline,
            context=message_info.context,
            box_id=message_info.box_id
        )
        self._s.add(entity)
        return entity

    def delete_mail(self, message_id: int, box_id: int):
        """删除信件"""
        statement = select(Message).where(Message.id == message_id and Message.box_id == box_id)
        resp = self._s.exec(statement).one()
        if not resp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到信件！"
            )
        self._s.delete(resp)
        return resp

    def get_mail_by_box_id(self, box_id: int):
        """
        拿到信箱下所有信件
        :param box_id:
        :return:
        """
        statement = select(Message).where(Message.box_id == box_id)
        resp: Iterable[Message] = self._s.exec(statement).all()
        return list(resp)

    def submit_mail_by_share_token(self, share_token: str, headline: str, context: str):
        """
        通过分享token匿名投递信件
        :param share_token:
        :param headline:
        :param context:
        :return:
        """
        # 查找信箱
        mailbox_statement = select(Mailbox).where(Mailbox.share_token == share_token)
        mailbox = self._s.exec(mailbox_statement).one()
        
        if not mailbox:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到信箱！"
            )
        
        # 创建信件
        message = Message(headline=headline, context=context, box_id=mailbox.id)
        self._s.add(message)
        return message