"""
Message CRUD services.
"""
from typing import Iterable

from fastapi import HTTPException
from sqlmodel import select
from starlette import status

from src.email_backend.schemes.dto import MessageInfo
from src.email_backend.schemes.entity import Mailbox, Message
from src.email_backend.services.serviceBase import ServiceBase


class MessageService(ServiceBase):
    def create_mail(self, message_info: MessageInfo):
        entity = Message(
            headline=message_info.headline,
            context=message_info.context,
            box_id=message_info.box_id,
        )
        self._s.add(entity)
        self._s.flush()
        self._s.refresh(entity)
        return entity

    def delete_mail(self, message_id: int, box_id: int):
        statement = select(Message).where(Message.id == message_id and Message.box_id == box_id)
        resp = self._s.exec(statement).one()
        if not resp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found",
            )
        self._s.delete(resp)
        return resp

    def get_mail_by_box_id(self, box_id: int):
        statement = select(Message).where(Message.box_id == box_id)
        resp: Iterable[Message] = self._s.exec(statement).all()
        return list(resp)

    def submit_mail_by_share_token(self, share_token: str, headline: str, context: str):
        mailbox_statement = select(Mailbox).where(Mailbox.share_token == share_token)
        mailbox = self._s.exec(mailbox_statement).one()

        if not mailbox:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mailbox not found",
            )

        message = Message(headline=headline, context=context, box_id=mailbox.id)
        self._s.add(message)
        self._s.flush()
        self._s.refresh(message)
        return message
