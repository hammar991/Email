"""
信件crud
"""
from src.email_backend.schemes.entity import Message

class MessageService:

    def create_mail(self, mailbox):
        """
        创建邮件
        """
        statement = Message(

        )

    def delete_mail(self, mailbox):
        pass

    def get_mail(self, mailbox):
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
