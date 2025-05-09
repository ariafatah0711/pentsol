import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATA_FILE = 'data/pentest_data.json'
EXCEL_FOLDER = 'data/excel'

# Search Configuration
SEARCH_ALGORITHMS = {
    'boyer_moore': 'Boyer-Moore Algorithm',
    'kmp': 'Knuth-Morris-Pratt Algorithm',
    'brute_force': 'Brute Force Algorithm'
}
DEFAULT_ALGORITHM = 'boyer_moore'
MAX_RESULTS = 5
MIN_SEARCH_LENGTH = 2

# Message Templates
MESSAGES = {
    'welcome': """
🚀 *Welcome to Pentest & Security Solutions Bot!* 🔍

Bot ini membantu kamu:
• 🔍 Cari teknik serangan
• 📖 Dapatkan solusi keamanan
• ⚡️ Info mitigasi
• 📊 Buat laporan solusi (CSV)

*Perintah utama:*
📌 `/search` – Cari teknik (misal: `/search sql injection`)
📌 `/describe` – Detail teknik (misal: `/describe sql injection`)
📌 `/list` – Lihat semua teknik
📌 `/create_solusi` – Buat laporan solusi (misal: `/create_solusi SQL Injection, XSS`)
📌 `/help` – Bantuan

💡 *Tip:* Gunakan kata kunci apapun, bot akan mencari yang paling relevan!
""",

    'help': """
🔰 *Panduan Penggunaan Bot* 🔰

*Perintah Utama:*
📌 `/search` – Cari teknik serangan
📌 `/describe` – Detail teknik
📌 `/list` – Lihat semua teknik
📌 `/create_solusi` – Buat laporan solusi (CSV)
📌 `/help` – Bantuan

*Contoh:*
• `/list`
• `/search sql injection`
• `/describe XSS Attack`
• `/create_solusi SQL Injection, XSS`

💡 *Tip:* Gunakan kata kunci apapun untuk mencari!
""",

    'errors': {
        'search_empty': "❌ *Masukkan kata kunci pencarian*\n\n📝 Contoh: `/search sql injection`",
        'search_not_found': "❌ *Tidak ditemukan hasil untuk:* `{query}`\n💡 Coba kata kunci lain atau gunakan `/list`",
        'describe_empty': "❌ *Masukkan nama teknik*\n\n📝 Contoh: `/describe XSS Attack`",
        'describe_not_found': "❌ *Teknik tidak ditemukan:* `{query}`\n💡 Coba `/list` untuk melihat semua teknik",
        'create_solusi_empty': "❌ *Masukkan nama teknik*\n\n📝 Contoh: `/create_solusi SQL Injection, XSS`",
        'technique_not_found': "❌ *Teknik tidak ditemukan:* `{name}`\n💡 Coba `/list` untuk melihat semua teknik",
        'no_token': "❌ BOT_TOKEN tidak ditemukan. Cek file .env"
    }
}

# File paths
EXCEL_TEMPLATE = 'data/excel/pentest_techniques_template.xlsx'
EXCEL_FILE = 'data.xlsx' 