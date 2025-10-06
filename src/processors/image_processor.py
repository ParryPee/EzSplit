"""
Image processor with OCR capabilities
"""
import logging
import os
from typing import Dict, Any, List
from .base_processor import BaseProcessor
from src.config import Config
from PIL import Image, ImageEnhance,ImageFilter
import cv2
import numpy as np
import requests

logger = logging.getLogger(__name__)


class ImageProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.supported_filetype = Config.SUPPORTED_FORMATS
        
    async def extract_text(self, file_path: str) -> str:
        
        try:
            r = requests.post(Config.ASPRISED_URL,
                              headers={
                                    'accept': 'application/json'},
                              files={"file": open(file_path,"rb")})
            result = r.json()
            
            self.cleanup_temp_file(file_path)
            
            if(not result['success']):
                return False
            else:
                return result['receipts'][0]
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            raise Exception(f"Failed to extract text from image: {str(e)}")
    
    async def split_bill(self, data):
        return await super().split_bill(data)
    


