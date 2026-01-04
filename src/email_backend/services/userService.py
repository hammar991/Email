"""
用户crud
"""
from sqlmodel import select

from src.email_backend.core.security import verify_password, password_hash
from src.email_backend.services.serviceBase import ServiceBase
from src.email_backend.schemes.entity import User
from src.email_backend.schemes.dto import UserInfo


class UserServices(ServiceBase):

    def create_user(self):
        """
        创建用户
        :return:
        """



    def modify_password(self):
        pass


    def authenticate_user(self, username: str, password: str):
        """
        验证用户
        :param username:
        :param password:
        :return:
        """
        statement = select(User).where(User.username == username)
        resp: User | None = self._s.exec(statement).one()        # 确保仅 能查找到一行数据,
        if not resp:
            return False
        return resp
