import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bot.handlers import start_handler, help_handler, llm_handler


@pytest.mark.asyncio
async def test_start_handler():
    """Тест обработчика команды /start"""
    # Создание мока сообщения
    message = AsyncMock()
    message.from_user.id = 12345
    message.from_user.username = "testuser"
    
    # Вызов обработчика
    await start_handler(message)
    
    # Проверка вызова reply
    message.reply.assert_called_once()
    args = message.reply.call_args[0]
    assert "Привет!" in args[0]
    assert "ИИ-ассистент" in args[0]
    assert "искусственный интеллект" in args[0]


@pytest.mark.asyncio
async def test_help_handler():
    """Тест обработчика команды /help"""
    message = AsyncMock()
    message.from_user.id = 12345
    
    await help_handler(message)
    
    message.reply.assert_called_once()
    args = message.reply.call_args[0]
    assert "Доступные команды:" in args[0]
    assert "/start" in args[0]
    assert "/help" in args[0]
    assert "искусственный интеллект" in args[0]


@pytest.mark.asyncio 
async def test_llm_handler_text_message():
    """Тест LLM обработчика с текстовым сообщением"""
    message = AsyncMock()
    message.from_user.id = 12345
    message.from_user.username = "testuser"
    message.text = "Тестовое сообщение"
    
    with patch('bot.handlers.call_llm', return_value="Ответ от LLM"):
        await llm_handler(message)
        
        message.reply.assert_called_once()
        args = message.reply.call_args[0]
        assert "Ответ от LLM" in args[0]


@pytest.mark.asyncio
async def test_llm_handler_non_text_message():
    """Тест LLM обработчика с не текстовым сообщением"""
    message = AsyncMock()
    message.from_user.id = 12345
    message.from_user.username = "testuser"
    message.text = None  # Не текстовое сообщение
    
    await llm_handler(message)
    
    message.reply.assert_called_once()
    args = message.reply.call_args[0]
    assert "только текстовые сообщения" in args[0]


@pytest.mark.asyncio
async def test_llm_handler_calls_llm():
    """Тест что LLM обработчик правильно вызывает call_llm"""
    message = AsyncMock()
    message.from_user.id = 12345
    message.from_user.username = "testuser"
    message.text = "Привет"
    
    with patch('bot.handlers.call_llm', return_value="Привет! Как дела?") as mock_call_llm:
        await llm_handler(message)
        
        # Проверяем что call_llm был вызван с правильными параметрами
        mock_call_llm.assert_called_once()
        call_args = mock_call_llm.call_args[0][0]
        
        assert len(call_args) == 2
        assert call_args[0]["role"] == "system"
        assert call_args[1]["role"] == "user"
        assert call_args[1]["content"] == "Привет"