"""
数据层：sqlmodel模型
"""
import uuid
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import Optional, List


class User(SQLModel, table=True):
    """用户表"""
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, index=True, primary_key=True)
    name: str = Field(default=None, max_length=255, unique=True)
    email: EmailStr = Field(default=None, unique=True, index=True, max_length=255)
    password: str = Field(default=None, min_length=8, max_length=255)

    mail_boxs: Optional[List["Mailbox"]] = Relationship(back_populates="user")


class Mailbox(SQLModel, table=True):
    """邮箱表"""
    __tablename__ = "mailbox"
    id: Optional[int] = Field(default=None, index=True, primary_key=True)
    box_name: EmailStr = Field(default=None, unique=True, index=True, max_length=255)
    share_token: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True, index=True, max_length=255)

    user_id: int = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="mail_boxs")
    messages: Optional["Message"] = Relationship(back_populates="mailbox")


class Message(SQLModel, table=True):
    """邮件表"""
    __tablename__ = "message"
    id: Optional[int] = Field(default=None, index=True, primary_key=True)
    headline: str = Field(default=None, max_length=255, unique=True)
    context: str | None = Field(max_length=255)

    box_id: int = Field(default=None, foreign_key="mailbox.id")
    mailbox: Optional["Mailbox"] = Relationship(back_populates="messages")


def init_db(engine):
    """创建所有数据库表"""
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    from src.email_backend.core.config import settings
    from sqlmodel import create_engine

    engine = create_engine(url=settings.DATABASE_URL, echo=True)
    print(engine)
    SQLModel.metadata.create_all(engine)
