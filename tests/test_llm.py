import pytest
from unittest.mock import AsyncMock, patch
from llm.client import call_llm


@pytest.mark.asyncio
async def test_call_llm_success():
    """Тест успешного вызова LLM"""
    # Создаем мок ответа
    mock_response = AsyncMock()
    mock_response.choices[0].message.content = "Тестовый ответ от LLM"
    
    with patch('llm.client.get_client') as mock_get_client:
        mock_client = AsyncMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [
            {"role": "system", "content": "Вы ассистент"},
            {"role": "user", "content": "Привет"}
        ]
        result = await call_llm(messages)
        
        assert result == "Тестовый ответ от LLM"


@pytest.mark.asyncio
async def test_call_llm_error_handling():
    """Тест обработки ошибки LLM"""
    with patch('llm.client.get_client') as mock_get_client:
        mock_client = AsyncMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_client
        messages = [
            {"role": "user", "content": "Привет"}
        ]
        result = await call_llm(messages)
        
        assert "ошибка" in result.lower()
        assert "извините" in result.lower()


@pytest.mark.asyncio
async def test_call_llm_empty_messages():
    """Тест с пустым списком сообщений"""
    mock_response = AsyncMock()
    mock_response.choices[0].message.content = "Пустой ответ"
    
    with patch('llm.client.get_client') as mock_get_client:
        mock_client = AsyncMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = []
        result = await call_llm(messages)
        
        assert isinstance(result, str)


@pytest.mark.asyncio
async def test_call_llm_logging():
    """Тест логирования запросов и ответов"""
    mock_response = AsyncMock()
    mock_response.choices[0].message.content = "Логируемый ответ"
    
    with patch('llm.client.get_client') as mock_get_client:
        mock_client = AsyncMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        with patch('llm.client.logger.info') as mock_logger:
            messages = [{"role": "user", "content": "Тест"}]
            await call_llm(messages)
            
            # Проверяем что логирование вызывалось
            assert mock_logger.call_count >= 2  # REQUEST и RESPONSE