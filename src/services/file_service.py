import logging
import os
import tempfile
from typing import Optional, Tuple
from telegram import Document, PhotoSize
from src.config import Config

logger = logging.getLogger(__name__)


class FileService:
    def __init__(self):
        self.temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(self.temp_dir, exist_ok=True)
        
    async def download_photo(self, photo: PhotoSize):
        file = await photo.get_file()
        
        file_name = f"photo_{photo.file_id}.jpg"
        
        return await self.download_telegram_file(file, file_name)
    
    
    async def download_telegram_file(self, telegram_file, original_filename: str = None) -> Tuple[str,str]:
        try:
            if original_filename:
                temp_file = tempfile.NamedTemporaryFile(
                    dir=self.temp_dir,
                    suffix=f"_{original_filename}",
                    delete=False
                )
            else:
                temp_file = tempfile.NamedTemporaryFile(
                    dir=self.temp_dir,
                    delete=False
                )
            
            temp_file.close()
            
            await telegram_file.download_to_drive(temp_file.name)
            filename = original_filename or os.path.basename(temp_file.name)
            logger.info(f"Downloaded Telegram file: {filename} -> {temp_file.name}")
            
            return temp_file.name, filename
            
        except Exception as e:
            logger.error(f"Error downloading Telegram file: {e}")
            raise Exception(f"Failed to download file: {str(e)}")
        
# Global instance
file_service = FileService()