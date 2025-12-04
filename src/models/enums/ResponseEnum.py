## for constants and enumerations
from enum import Enum 
class ResponseSignal(Enum):

    FILE_VALIDATED = "File validated successfully"
    FILE_TYPE_INVALID = "Invalid file type"
    FILE_SIZE_EXCEEDED = "File size exceeds the limit"
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_UPLOAD_FAILED = "File upload failed"
    PROCESSING_FAILED = "File processing failed"
    PROCESSING_SUCCESS = "File processed successfully"
