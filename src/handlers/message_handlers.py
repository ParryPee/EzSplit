import logging
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from src.config import Config
from src.services.file_service import file_service
from src.processors.image_processor import ImageProcessor




logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = """
    **Welcome to Re-Split bot!**
    
    This bot will help to scan your receipts and split the bills accordingly.
    
    **Supported formats**
    Images: PNG,JPEG, JPG
    Documents: *Coming soon*
    
    
    
    """
    print("here")
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown'
    )
    
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = """
    🆘 **Help & Support**

    **What does this bot do?**
    I scan your receipts before helping you to split them!
    Easy to use
    Efficient splitting

    **Privacy & Security:**
    - All processing happens locally on our server
    - Files are temporarily stored only during processing
    - No data is shared with third parties
    - Files are automatically deleted after processing

    **Supported file types:**
    - **Documents:** Coming soon
    - **Images:** JPEG, PNG, JPG

    **File size limit:** 20MB per file
    
    """
    
    await update.message.reply_text(
        help_message,
        parse_mode='Markdown'
    )
    
    
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo = update.message.photo[-1]

    if not photo:
        await update.message.reply_text("❌ No photo received. Please try again.")
        return
    
        

    processing_msg = await update.message.reply_text(
        "🔄 Processing your image...\nExtracting text and prices"
    )


    try:
        file_path, file_name = await file_service.download_photo(photo=photo)
        processor = ImageProcessor()
        texts = await processor.extract_text(file_path)
        
        print(texts)
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        await processing_msg.edit_text(
            "❌ Error processing document. Please try again later."
        )
async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown/unsupported message types"""
    await update.message.reply_text(
        "❓ I can only process images.\n\n"
        "Please send me:\n"
        "🖼️ Images: JPG, PNG\n\n"
        "Or use /help for more information."
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Exception while handling an update: {context.error}")
    
    if update and hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            "❌ An unexpected error occurred. Please try again later."
        )