"""
信件crud
"""

from src.email_backend.services.serviceBase import ServiceBase
from src.email_backend.schemes.entity import Message
from src.email_backend.schemes.dto import MessageInfo

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


    def delete_mail(self,  message_info: MessageInfo):
        """
        删除信件
        """
        pass

    def get_mail(self,  message_info: MessageInfo):
        """拿到所有mail"""
        pass

    def get_mail_by_headline(self, headline : str):
        """
        按照标题查找邮件
        """
        pass


    # def update_mail(self, mailbox):
    #     pass
    #     """更新信件"""
