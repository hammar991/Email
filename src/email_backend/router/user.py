"""
用户接口
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["用户接口"]
)

@router.get("/userinfo")
def get_user():
    pass


@router.post("/userinfo")
def update_user():
    pass
