from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def handle_ocr_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    
    ocr_text = context.user_data['ocr_text']
    
    
    
    if query.data == 'confirm_ocr':
        # User confirmed the OCR text
        await query.edit_message_text(text=f"✓ Confirmed!\n\n")
        # Continue to next processing steps here
        
    elif query.data == 'edit_ocr':
        # User wants to edit the text
        await query.edit_message_text(text="Please send the corrected text:")
        # Set a flag in context to expect corrected text
        context.user_data['awaiting_correction'] = True
