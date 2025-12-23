"""
数据层：数据库orm操作
"""
from sqlmodel import SQLModel, Field, create_engine, Integer
from pydantic import EmailStr

from src.email_backend.config.config import settings


class User(SQLModel, table=True):
    """用户表"""
    __tablename__ = "user"
    id: int = Field(default=Integer, index=True, primary_key=True)
    name: str = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password: str = Field(default=None, min_length=8, max_length=255)


class Mailbox(SQLModel, table=True):
    """邮箱表"""
    __tablename__ = "mailbox"
    id: int = Field(default=Integer, index=True, primary_key=True)
    box_name = str
    user_id: int = Field(default=None, foreign_key="user.id")


class Message(SQLModel, table=True):
    """邮件表"""
    __tablename__ = "message"
    id: int = Field(default=Integer, index=True, primary_key=True)
    context: str | None = Field(max_length=255)
    box_id: int = Field(default=Integer, foreign_key="mailbox.id")


# 创建数据库引擎
engine = create_engine(f"{settings.DATABASE_URL}", echo=True)
# 创建所有数据库表
SQLModel.metadata.create_all(engine)