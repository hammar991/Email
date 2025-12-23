"""
邮箱接口
"""

from fastapi import APIRouter

router = APIRouter(
    prefix = "/box",
    tags=["邮箱接口"]
)


@router.get("/mailbox")
def get_mailbox():
    pass

@router.post("/create_mailbox")
def create_mailbox():
    pass

@router.post("/mailbox")
def modify_mailbox():
    pass

@router.delete("/mailbox")
def get_mailbox():
    pass

@router.get("/share_mailbox")
def share_mailbox():
    pass