import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# LLM Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "anthropic/claude-3.5-sonnet")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "500"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def validate_config():
    """Валидация обязательных параметров конфигурации"""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is required. Check your .env file.")
    
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is required. Check your .env file.")