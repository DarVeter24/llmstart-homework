import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from llm.client import call_llm

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start_handler(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    logger.info(f"User {user_id} ({username}) started bot")
    
    welcome_text = (
        "Привет! Я ИИ-ассистент для консультаций.\n"
        "Теперь я использую искусственный интеллект для ответов!\n"
        "Задавайте любые вопросы, и я постараюсь помочь."
    )
    
    await message.reply(welcome_text)


@router.message(Command("help"))
async def help_handler(message: Message):
    """Обработчик команды /help"""
    user_id = message.from_user.id
    logger.info(f"User {user_id} requested help")
    
    help_text = (
        "Доступные команды:\n"
        "/start - Начать диалог с ассистентом\n"
        "/help - Получить эту справку\n\n"
        "Я использую искусственный интеллект для ответов на ваши вопросы.\n"
        "Просто напишите мне что-нибудь, и я постараюсь помочь!"
    )
    
    await message.reply(help_text)


@router.message()
async def llm_handler(message: Message):
    """Обработчик сообщений через LLM"""
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    message_text = message.text or "[не текстовое сообщение]"
    
    logger.info(f"LLM message from user {user_id} ({username}): {message_text[:50]}...")
    
    # Простая проверка на не текстовые сообщения
    if not message.text:
        await message.reply("Пока что я умею обрабатывать только текстовые сообщения.")
        return
    
    # Простой запрос к LLM без истории диалога (пока)
    messages = [
        {
            "role": "system", 
            "content": "Вы дружелюбный и полезный ассистент. Отвечайте кратко, по делу и на русском языке. Помогайте пользователям с их вопросами."
        },
        {
            "role": "user", 
            "content": message_text
        }
    ]
    
    # Отправляем запрос к LLM
    response = await call_llm(messages)
    await message.reply(response)