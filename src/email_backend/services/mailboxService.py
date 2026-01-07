"""
邮箱crud
"""
from sqlmodel import select
from src.email_backend.schemes.entity import Mailbox
from src.email_backend.services.serviceBase import ServiceBase


class MailboxService(ServiceBase):

    def create_mailbox(self, mailbox):
        pass

    def delete_mailbox(self, mailbox):
        pass

    def update_mailbox(self, mailbox):
        pass

    def get_mailbox_by_user_id(self, uid : int):
        """
        拿到用户下所有邮箱
        :param uid:
        :return:
        """
        statement = select(Mailbox).where(Mailbox.user_id == uid)
        resp = self._s.exec(statement)
        return resp