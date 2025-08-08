import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bot.handlers import (
    start_handler,
    help_handler,
    llm_handler,
    conversation_history,
    services_handler,
)


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
        
        assert len(call_args) >= 2
        assert call_args[0]["role"] == "system"
        assert call_args[-1]["role"] == "user"
        assert call_args[-1]["content"] == "Привет"


@pytest.mark.asyncio
async def test_llm_handler_uses_history():
    """Второе сообщение должно передаваться в LLM с контекстом истории"""
    conversation_history.clear()

    # Первое сообщение
    msg1 = AsyncMock()
    msg1.from_user.id = 999
    msg1.from_user.username = "u"
    msg1.text = "Первый вопрос"

    with patch('bot.handlers.call_llm', return_value="Первый ответ"):
        await llm_handler(msg1)

    # Второе сообщение
    msg2 = AsyncMock()
    msg2.from_user.id = 999
    msg2.from_user.username = "u"
    msg2.text = "Второй вопрос"

    with patch('bot.handlers.call_llm', return_value="Второй ответ") as mock_call:
        await llm_handler(msg2)
        sent_messages = mock_call.call_args[0][0]
        assert sent_messages[0]["role"] == "system"
        roles = [m["role"] for m in sent_messages[1:]]
        assert roles == ["user", "assistant", "user"]


@pytest.mark.asyncio
async def test_services_handler():
    message = AsyncMock()
    message.from_user.id = 1
    await services_handler(message)
    message.reply.assert_called_once()
    assert "Доступные услуги" in message.reply.call_args[0][0]


@pytest.mark.asyncio
async def test_name_capture_and_reply():
    # Очистка истории
    conversation_history.clear()

    # Имитируем короткое имя как первую реплику
    msg = AsyncMock()
    msg.from_user.id = 42
    msg.from_user.username = "u"
    msg.text = "Андрей"
    await llm_handler(msg)

    # Должен ответить без вызова LLM и не падать
    msg.reply.assert_called_once()
    assert "Приятно познакомиться" in msg.reply.call_args[0][0]