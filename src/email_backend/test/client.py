from requests import Session
from loguru import logger

from src.email_backend.schemes.dto import RegisterMsg, LoginMsg
from src.email_backend.core.config import SETTINGS


class Client:
    def __init__(self, endpoint: str = "http://localhost:8003", timeout=30):
        self.endpoint = f"{endpoint}{SETTINGS.api_v1_str}"
        self.session = Session()
        self.token = None
        self.timeout = timeout
        self.username = None
        self.password = None

    def register_user(self, msg=RegisterMsg):
        try:
            return self.session.post(f"{self.endpoint}/user/register", data=msg)
        except Exception as e:
            logger.exception(e)
            repr(e)

    def login(self, username: str, password: str):
        data = {"username": username, "password": password}
        try:
            response = self.session.post(f"{self.endpoint}/user/login/access-token", data=data)
            response.raise_for_status() # 抛出异常错误
            self.token = response.json()["access_token"]
            self.username = username
            self.password = password
            return response
        except Exception as e:
            logger.exception(e)
            repr(e)

    def reset_password(self):
        pass

