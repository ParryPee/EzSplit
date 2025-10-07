import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler,ConversationHandler 
from src.config import Config
from src.handlers.message_handlers import (
    start_command,
    help_command,
    split_command,
    cancel_upload,
    handle_photo,
    handle_unknown,
    error_handler
)



from src.handlers.callback_handler import handle_ocr_callback

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if not Config.DEBUG else logging.DEBUG
)
logger = logging.getLogger(__name__)


def main() -> None:
    try:
        Config.validate()

        logger.info("Starting Telegram Resplit Bot...")
        
        # Create application
        app = Application.builder().token(Config.TELEGRAM_TOKEN).build()
        
        #Add command handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        
        #Add callback handler
        app.add_handler(CallbackQueryHandler(handle_ocr_callback))

        #Add conversation handlers
        conv_handler = ConversationHandler(
        entry_points=[CommandHandler('split', split_command)],
        states={
            Config.WAITING_FOR_IMAGE: [
                MessageHandler(filters.PHOTO, handle_photo)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel_upload)]
    )
        app.add_handler(conv_handler)
        # Handle unknown message types
        app.add_handler(MessageHandler(
            ~(filters.COMMAND | filters.Document.ALL | filters.PHOTO), 
            handle_unknown
        ))
        
        # Add error handler
        app.add_error_handler(error_handler)
        
        logger.info("Bot setup complete. Starting polling...")
        
        # Start the bot
        app.run_polling(allowed_updates=["message","callback_query"])

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ Configuration Error: {e}")
        print("\n📝 Setup Instructions:")
        print("1. Copy '.env.example' to '.env'")
        print("2. Add your Telegram bot token to the .env file")
        print("3. Make sure Ollama is running: 'ollama serve'")
        print("4. Pull the required model: 'ollama pull llama3.2:3b'")
        
    except Exception as e:
        logger.error(f"Unexpected error starting bot: {e}")
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()