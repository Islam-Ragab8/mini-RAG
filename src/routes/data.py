from fastapi import FastAPI,APIRouter, Depends,UploadFile
from helpers.config import get_settings, Settings
from controllers import DataController

data_router = APIRouter(
    prefix="/data",
    tags=["data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str, file: UploadFile, app_setting:Settings = Depends(get_settings)):
    is_valid=DataController().validate_file(file=file)
    return is_valid 