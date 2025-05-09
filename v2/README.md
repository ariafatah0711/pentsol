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
# Build the Docker image
docker build -t bot_pentest_suggest .

# Run the bot in a container
docker run -it --rm --name bot_pentest_suggest -v ./:/app -v ./log/docker:/app/log bot_pentest_suggest

# or with alias
```

---

## 🖥️ Setup Using a Virtual Environment
```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make the bot executable
chmod +x main.py
```

---

## 🚀 Setup Using Pyenv + Virtual Environment
```bash
# Install pyenv
curl https://pyenv.run | bash

# Configure shell
cat >> ~/.bashrc << 'EOF'
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
EOF

exec $SHELL

# Install Python and set global version
pyenv install 3.12.8
pyenv global 3.12.8

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make the bot executable
chmod +x main.py

# Run the bot
./main.py
```

---

## ▶️ Running the Bot
```bash
# Run the bot
python main.py

# Or, if using a virtual environment
./main.py
```

## 🔧 Additional Options
```bash
./main.py # Run the bot with default settings
./main.py --setup # generate template
```

---

## 🛠️ Cleanup (Optional)
```bash
# Remove Python cache files
find . -name "__pycache__" -o -name "*.pyc" | xargs rm -rf

# reset data excel
rm -rf data/*
```