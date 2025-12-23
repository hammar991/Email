

from fastapi import FastAPI

from src.email_backend.config.config import Settings


app = FastAPI(
    title=Settings.TITLE
)

