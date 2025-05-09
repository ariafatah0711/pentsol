import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATA_FILE = 'data/pentest_data.json'
EXCEL_FOLDER = 'data/excel'

# Search Configuration
SEARCH_THRESHOLD = 60  # Minimum similarity score for fuzzy search
MAX_RESULTS = 5  # Maximum number of results to show

# Message Templates
MESSAGES = {
    'welcome': """
🚀 *Welcome to Pentest & Security Solutions Bot!* 🔍

This bot helps you with:
• 🔍 Search attack techniques
• 📖 Get security solutions
• ⚡️ Get mitigation information
• 📊 Create solution reports in CSV format

Use these commands:
📌 `/search` – Search techniques (e.g. `/search sql injection`)
📌 `/describe` – Get technique details (e.g. `/describe sql injection`)
📌 `/list` – View all techniques
📌 `/create_solusi` – Create solution report in CSV (e.g. `/create_solusi SQL Injection, XSS`)
📌 `/help` – Show this help message

💡 Tip: Use any keywords, the bot will find similar matches!
""",

    'help': """
🔰 *Bot Usage Guide* 🔰

*Basic Commands:*
📌 `/search` – Search attack techniques
📌 `/describe` – Get technique details
📌 `/list` – View all techniques
📌 `/create_solusi` – Create solution report in CSV
📌 `/help` – Show this help message

*Usage Examples:*
• `/list`
• `/search sql injection`
• `/describe XSS Attack`
• `/create_solusi SQL Injection, XSS`

💡 Tip: Use any keywords for searching!
""",

    'errors': {
        'search_empty': "❌ *Please enter search keywords*\n\n📝 Example: `/search sql injection`",
        'search_not_found': "❌ *No results found for:* `{query}`\n💡 Try different keywords or use `/list`",
        'describe_empty': "❌ *Please enter technique name*\n\n📝 Example: `/describe XSS Attack`",
        'describe_not_found': "❌ *Technique not found:* `{query}`\n💡 Try `/list` to see all techniques",
        'create_solusi_empty': "❌ *Please enter technique names*\n\n📝 Example: `/create_solusi SQL Injection, XSS`",
        'technique_not_found': "❌ *Technique not found:* `{name}`\n💡 Try `/list` to see all techniques"
    }
}