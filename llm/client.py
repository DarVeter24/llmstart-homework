import logging
from openai import AsyncOpenAI
from config import (
    OPENROUTER_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    OPENROUTER_HTTP_REFERER,
    OPENROUTER_APP_TITLE,
)

logger = logging.getLogger(__name__)

# Клиент будет инициализирован при первом вызове
_client = None


def get_client():
    """Получение клиента OpenRouter с ленивой инициализацией"""
    global _client
    if _client is None:
        headers = {}
        if OPENROUTER_HTTP_REFERER:
            headers["HTTP-Referer"] = OPENROUTER_HTTP_REFERER
        if OPENROUTER_APP_TITLE:
            headers["X-Title"] = OPENROUTER_APP_TITLE

        _client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            default_headers=headers or None,
        )
    return _client


async def call_llm(messages: list) -> str:
    """Отправляет запрос к LLM через OpenRouter"""
    try:
        logger.info(f"LLM_REQUEST: messages_count={len(messages)}")
        
        client = get_client()
        response = await client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS
        )
        
        content = response.choices[0].message.content
        logger.info(f"LLM_RESPONSE: response_length={len(content)}")
        
        return content
        
    except Exception as e:
        logger.error(f"LLM_ERROR: {str(e)}")
        return "Извините, произошла ошибка при обработке запроса."