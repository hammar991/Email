"""
邮箱crud
"""
from fastapi import Depends
from sqlmodel import Session

from src.email_backend.schemes.entity import User
from src.email_backend.services.userService import UserServices
from src.email_backend.services.serviceBase import ServiceBase


class MailboxService(ServiceBase):

    def __init__(self, session):
        super(MailboxService, self).__init__(session)

        self.user_service = UserServices(self._s)
        self.current_user: User = Depends(self.user_service.get_current_user)


    def create_mailbox(self, mailbox):
        pass

    def delete_mailbox(self, mailbox):
        pass

    def update_mailbox(self, mailbox):
        pass

    def get_mailbox(self, mailbox):
        pass