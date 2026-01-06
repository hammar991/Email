"""
用户crud
"""

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import func
from sqlmodel import select

from src.email_backend.core.security import get_password_hash
from src.email_backend.schemes.dto import RegisterMsg
from src.email_backend.schemes.entity import User
from src.email_backend.services.serviceBase import ServiceBase


class UserServices(ServiceBase):

    def create_user(self, data: RegisterMsg):
        """
        创建用户
        :return:
        """
        # 加密密码
        data.password = get_password_hash(data.password)

        num = self._s.exec(select(func.count()).select_from(User)).one()

        logger.debug(f"num:{num} \n data:{data}")

        if num > 0:
            # 重名
            statement = select(User).where(User.name == data.name)
            resp = self._s.exec(statement).first()
            if resp:
                raise HTTPException(
                    status_code=401,
                    detail="用户名已存在!"
                )

        # 插入数据
        statement2 = User(name=data.name, email=data.email, password=data.password)
        print(statement2)
        self._s.add(statement2)
        return True

    def modify_password(self):
        pass

    @logger.catch()
    def authenticate_user(self, username: str, password: str):
        """
        验证用户
        :param username:
        :param password:
        :return:
        """
        statement = select(User).where(User.name == username)
        resp: User | None = self._s.exec(statement).one()  # 确保仅 能查找到一行数据,
        if not resp:
            return False
        return resp
