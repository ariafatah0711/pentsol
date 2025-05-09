import sys
import os
from handlers import register_handlers
from config import BOT_TOKEN, DATA_FILE
from utils.create_templates import create_all_templates
from utils.excel_to_json import convert_all_excel_to_json

def log_info(message):
    print(f"[!] {message}")

def log_error(message):
    print(f"[X] {message}")

def setup_data():
    """Setup data directory and create templates if needed"""
    # Create data directory if not exists
    if not os.path.exists('data'):
        os.makedirs('data')
        log_info("Created data directory")

    # Create excel directory if not exists
    excel_dir = 'data/excel'
    if not os.path.exists(excel_dir):
        os.makedirs(excel_dir)
        log_info("Created excel directory")

    # Check if data file exists
    if not os.path.exists(DATA_FILE):
        log_info("Data file not found, creating templates...")
        try:
            create_all_templates()
            log_info("Templates created successfully")
            
            # Convert Excel to JSON
            log_info("Converting Excel to JSON...")
            if convert_all_excel_to_json():
                log_info("Data conversion completed")
            else:
                log_error("Failed to convert Excel to JSON")
                sys.exit(1)
        except Exception as e:
            log_error(f"Error creating templates: {e}")
            sys.exit(1)

def main():
    # Setup data
    setup_data()

    # Check token
    if not BOT_TOKEN:
        log_error("BOT_TOKEN not found. Please set it in .env file")
        sys.exit(1)

    log_info("Starting bot...")
    try:
        bot = register_handlers()
        log_info("Bot is running...")
        bot.polling(none_stop=True)
    except Exception as e:
        log_error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 