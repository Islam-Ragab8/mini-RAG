from fastapi import FastAPI,APIRouter, Depends,UploadFile , status 
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController
from controllers import ProjectController
from models import ResponseSignal
import aiofiles
import os
import logging

logger = logging.getLogger("uvicorn.error")



data_router = APIRouter(
    prefix="/data",
    tags=["data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str, file: UploadFile, app_setting:Settings = Depends(get_settings)):
    is_valid, result_signal = DataController().validate_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path=DataController().generate_unique_filename(
        original_filename=file.filename,      
        project_id=project_id          
    )

    try:
        async with aiofiles.open(file_path,'wb') as f:
            while chunk := await file.read(app_setting.FILE_DEFAULT_CHUNK_SIZE):
               await f.write(chunk)
    except Exception as e:

        logger.error(f"File upload error: {e}")
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={
            "signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value, 
        }   
    )