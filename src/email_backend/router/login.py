"""
登录接口
"""
from fastapi import APIRouter


router = APIRouter(
    prefix="/",
    tags=["登录注册接口"]
)

@router.post("login/access-token")
def login():
    pass


@router.post("register")
def register_user():
    pass