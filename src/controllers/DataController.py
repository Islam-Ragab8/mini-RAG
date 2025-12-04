### logic folder data in routes

from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import os


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1024*1024  # MB
    
    def validate_file(self, file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False , ResponseSignal.FILE_TYPE_INVALID.value
        
        if file.size > self.app_settings.MAX_FILE_SIZE*self.size_scale :
            return False , ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True , ResponseSignal.FILE_VALIDATED.value
    
    def generate_unique_filepath(self, original_filename:str , project_id: str):
        random_filename=self.generate_random_string()
        project_path=ProjectController().get_project_path(project_id=project_id)
        cleaned_filename=self.get_clean_filename(original_filename=original_filename)

        new_file_path=os.path.join(
            project_path,
            f"{random_filename}_{cleaned_filename}"
        )

        while os.path.exists(new_file_path):
            random_filename=self.generate_random_string()
            new_file_path=os.path.join(
                project_path,
                f"{random_filename}_{cleaned_filename}"
            ) # regenerate if exists

        return new_file_path, random_filename+"_"+cleaned_filename

    def get_clean_filename(self, original_filename:str):

        cleaned_filename=re.sub(r'[^\w.]', '', original_filename)
        cleaned_filename=cleaned_filename.replace(" ","_").lower()
        return cleaned_filename
       