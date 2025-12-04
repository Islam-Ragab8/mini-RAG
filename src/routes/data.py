from fastapi import FastAPI,APIRouter, Depends,UploadFile , status 
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController
from controllers import ProjectController, ProcessController
from models import ResponseSignal
from .schemas.data import ProcessRequest
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
    file_path , file_id = DataController().generate_unique_filename(
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
            "file_id":file_id
        }   
    )

@data_router.post("/process/{project_id}")
async def process_data(project_id:str, process_request:ProcessRequest):

    file_id=process_request.file_id
    process_controller=ProcessController(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)

    file_chunks=process_controller.process_file_content(
        file_content=file_content,      
        file_id=file_id,
        chunk_size=process_request.chunk_size,
        overlap_size=process_request.overlap_size)
    
    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.PROCESSING_FAILED.value
            }
        )
    return file_chunks
    
    