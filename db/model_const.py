from enum import Enum


class FileStatus(str, Enum):
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"

    UPLOAD_FAILED = "upload_failed"
    PROCESSING_FAILED = "processing_failed"
