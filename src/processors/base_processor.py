from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import tempfile
import os
import logging
from src.config import Config


logger = logging.getLogger(__name__)

class BaseProcessor(ABC):
    
    def __init__(self):
        self.supported_filetype = []
        self.max_filesize = 20
    
    @abstractmethod
    async def extract_text(self, file_path: str) -> str:
        
        pass
    
    @abstractmethod
    async def split_bill(self, receipt_data: str)-> bool:
        pass


    async def create_temp_file(self, original_filename: str) -> str:
        """Create a temporary file for processing"""
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_file = tempfile.NamedTemporaryFile(
            dir=temp_dir,
            suffix=f"_{original_filename}",
            delete=False
        )
        temp_file.close()
        return temp_file.name

    def validate_file_size(self, file_size: int) -> bool:
        """Validate file size is within limits"""
        
        return file_size <= Config.MAX_FILE_SIZE_MB
    
    def cleanup_temp_file(self, file_path: str) -> None:
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temp file {file_path}: {e}")