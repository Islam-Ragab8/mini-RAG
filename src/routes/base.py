from fastapi import APIRouter, FastAPI
import os
# from dotenv import load_dotenv
# load_dotenv()
from helpers.config import get_settings

base_router = APIRouter()

@base_router.get("/")
async def welcome():
    settings= get_settings()
    app_name = settings.APP_NAME.value
    app_version = settings.APP_VERSION.value
    return {

        "app_name": app_name,
        "app_version": app_version,
        "message": "Welcome to the API!",
    }