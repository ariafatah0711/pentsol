FROM python:3.12.8-slim

# Set working directory
WORKDIR /app

# Copy only essential files
COPY req.txt .

# Install dependencies
RUN pip install --no-cache-dir -r req.txt

# Command to run the application
CMD ["python", "bot.py"]