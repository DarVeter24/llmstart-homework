import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# LLM Configuration
OPENROUTER_API_KEY = (os.getenv("OPENROUTER_API_KEY") or "").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "anthropic/claude-3.5-sonnet")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "500"))
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "Вы дружелюбный и полезный ассистент. Отвечайте кратко, по делу и на русском языке. Помогайте пользователям с их вопросами.",
)
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "10"))
OPENROUTER_HTTP_REFERER = os.getenv("OPENROUTER_HTTP_REFERER", "")
OPENROUTER_APP_TITLE = os.getenv("OPENROUTER_APP_TITLE", "LLMStartTest")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def validate_config():
    """Валидация обязательных параметров конфигурации"""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is required. Check your .env file.")
    
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is required. Check your .env file.")