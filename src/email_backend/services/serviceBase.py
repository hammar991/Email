"""
@File: serviceBase.py
@Description: 基类
"""

from sqlmodel import Session

class ServiceBase:
    def __init__(self, session: Session):
        self._s = session