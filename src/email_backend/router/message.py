"""
邮件接口
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/message",
    tags=["邮件接口"]
)

@router.get("/show")
def get_message():
    pass


@router.post("/send")
def send_message():
    pass

@router.post("/message")
def modify_message():
    pass

@router.delete("/message")
def delete_message():
    pass


