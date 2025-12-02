### logic files
from .BaseController import BaseController
from fastapi import UploadFile
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1024*1024  # MB
    
    def validate_file(self, file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False
        
        if file.size > self.app_settings.MAX_FILE_SIXE*self.size_scale :
            return False
        
        return True