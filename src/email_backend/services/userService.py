"""
用户crud
"""
import jwt, jose
from fastapi import HTTPException, Depends
from loguru import logger
from sqlalchemy import func
from sqlmodel import select
from typing import Annotated

from src.email_backend.core.security import get_password_hash
from src.email_backend.core.config import settings
from src.email_backend.schemes.dto import RegisterMsg, CredentialResponse, UserResetMsg
from src.email_backend.schemes.entity import User
from src.email_backend.services.serviceBase import ServiceBase
from src.email_backend.core.security import oauth2_scheme


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

    def reset_password(self, data: UserResetMsg):
        """
        重置密码
        :return:
        """
        statement = select(User).where(User.name == data.name and User.email == data.email)
        resp = self._s.exec(statement).one()

        if not resp:
            raise HTTPException(
                status_code=404,
                detail="未找到数据！请检查用户名和邮箱！！"
            )

        if not data.password == data.ensure_password:
            raise HTTPException(
                status_code=404,
                detail="确认密码和重置密码不一致，请重新输入！"
            )

        # 更新密码
        resp.password =data.password
        # 添加到会话
        self._s.add(resp)
        return True


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

    def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        """
        拿到当前用户
        :return:
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
            username: str = payload.get("sub")
            if username is None:
                raise CredentialResponse
        except jose.JWTError:
            raise CredentialResponse

        # 验证用户是否存在
        user = self._s.exec(select(User).where(User.name == username)).one()
        if not user:
            raise CredentialResponse
        return user