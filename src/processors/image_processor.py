"""
Image processor with OCR capabilities
"""
import logging
import os
from typing import Dict, Any, List
from .base_processor import BaseProcessor
from src.config import Config
import pytesseract
from PIL import Image, ImageEnhance,ImageFilter
import cv2

logger = logging.getLogger(__name__)


class ImageProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.supported_filetype = Config.SUPPORTED_FORMATS
        
    async def extract_text(self, file_path: str) -> str:
        
        try:
            pytesseract.pytesseract.tesseract_cmd = fr'{Config.TESSERACT_PATH}'
            processed_image = self.preprocess_image(file_path)
            data = pytesseract.image_to_data(processed_image,output_type=pytesseract.Output.DICT)
            
            texts = data['text']
            confidence = data['conf']
            # Filter out empty text entries and pair them with confidence
            results = [(text, int(conf)) for text, conf in zip(texts, confidence) if text.strip() != '' and int(conf) > 0]
            print(results)
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            raise Exception(f"Failed to extract text from image: {str(e)}")
    
    async def split_bill(self, file_path):
        return await super().split_bill(file_path)
    
    
    def preprocess_image(self, image_path):
        # Load grayscale image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Upscale image (e.g., 2x)
        upscaled = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Convert to PIL for enhancing
        pil_img = Image.fromarray(upscaled)

        # Slightly sharpen image
        sharpened = pil_img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(sharpened)
        enhanced_img = enhancer.enhance(1.5)

        return enhanced_img

