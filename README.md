# 📌 Setup Guide for PenBot "Pentest Bot"

## 🪞 Clone the Repository
```bash
git clone <repository_url>
cd <repository_folder>
```

## 🔑 Setting Up the Telegram Bot Token
1. Create a new bot using [@BotFather](https://t.me/BotFather) on Telegram.
2. Follow the instructions to obtain your bot API token.
3. Create a `.env` file and add your bot token:
   ```sh
   BOT_TOKEN=<your_token_here>
   ```

---

## 🐳 Running with Docker
```bash
cd v1 # or v2
./pentsol
```

---

## 🛠️ Cleanup (Optional)
```bash
# Remove Python cache files
find . -name "__pycache__" -o -name "*.pyc" | xargs rm -rf

# reset data excel
rm -rf data/*
```