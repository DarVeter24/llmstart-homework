import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from llm.client import call_llm
from config import SYSTEM_PROMPT, MAX_HISTORY_MESSAGES

router = Router()
logger = logging.getLogger(__name__)
conversation_history: dict[int, list[dict]] = {}
user_profiles: dict[int, dict] = {}

# Базовый список услуг (KISS). Можно расширять/переносить в конфиг.
SERVICES: list[str] = [
    "Первичная консультация по МЛ/LLM и продуктовой идее",
    "Проектирование и внедрение телеграм-ботов на базе LLM",
    "Настройка экспериментов и трекинга (MLflow)",
    "CI/CD и контейнеризация (Docker) для ML-сервисов",
    "Мониторинг качества и метрик LLM",
]

def _is_likely_name(text: str) -> bool:
    if not text:
        return False
    t = text.strip()
    t_lower = t.lower()
    # Частые приветствия/слова, которые не являются именами
    non_names = {
        "привет", "здравствуйте", "здарова", "салют", "добрый", "доброго",
        "пока", "спасибо", "ок", "алло", "йо", "хай", "hello", "hi",
    }
    if t_lower in non_names:
        return False
    # Имя: одно слово, без цифр и спецсимволов, первая буква заглавная, длина до 20
    if " " in t or "\t" in t or "\n" in t:
        return False
    if not t[:1].isalpha() or not t[:1].istitle():
        return False
    if not all(ch.isalpha() or ch in "-" for ch in t):
        return False
    return 1 <= len(t) <= 20


@router.message(Command("start"))
async def start_handler(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    logger.info(f"User {user_id} ({username}) started bot")
    # Сброс истории и установка системного промпта
    conversation_history[user_id] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    welcome_text = (
        "Привет! Я ИИ-ассистент для консультаций.\n"
        "Теперь я использую искусственный интеллект для ответов!\n"
        "Задавайте любые вопросы, и я постараюсь помочь.\n\n"
        "Как я могу к вам обращаться? Напишите ваше имя и мы продолжим."
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
        "/services - Показать список услуг\n"
        "/help - Получить эту справку\n\n"
        "Я использую искусственный интеллект для ответов на ваши вопросы.\n"
        "Просто напишите мне что-нибудь, и я постараюсь помочь!"
    )
    await message.reply(help_text)


@router.message(Command("services"))
async def services_handler(message: Message):
    user_id = message.from_user.id
    logger.info(f"User {user_id} requested services list")
    services_text = "\n".join(f"- {s}" for s in SERVICES)
    await message.reply(f"Доступные услуги:\n{services_text}")


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
    
    # Обработка знакомства с клиентом: первая короткая реплика после /start — как имя
    profile = user_profiles.get(user_id, {})
    if "name" not in profile and _is_likely_name(message_text):
        profile["name"] = message_text.strip()
        user_profiles[user_id] = profile
        await message.reply(
            f"Приятно познакомиться, {profile['name']}! Напишите /services, чтобы увидеть список услуг, или задайте вопрос."
        )
        return

    # Подготовка/инициализация истории
    history = conversation_history.get(user_id)
    if not history:
        history = [{"role": "system", "content": SYSTEM_PROMPT}]
        conversation_history[user_id] = history

    # Добавляем текущее сообщение пользователя
    history.append({"role": "user", "content": message_text})

    # Формируем хвост истории без системного промпта
    tail = history[1:][-MAX_HISTORY_MESSAGES * 2 :]
    messages = [history[0]] + tail

    # Если знаем имя — добавим вспомогательный system для персонизации
    if "name" in profile:
        messages = (
            [{"role": "system", "content": f"Имя пользователя: {profile['name']}"}] + messages
        )

    # Если вопрос про услуги — добавим подсказку с каталогом
    lower = message_text.lower()
    if any(k in lower for k in ["услуг", "услуга", "стоим", "цена", "консультируешь"]):
        catalog = "\n".join(f"- {s}" for s in SERVICES)
        messages = (
            [{"role": "system", "content": f"Список услуг компании:\n{catalog}\nОтвечайте только на основе этого списка и кратко."}]
            + messages
        )
    
    # Отправляем запрос к LLM
    response = await call_llm(messages)
    # Добавляем ответ ассистента в историю
    history.append({"role": "assistant", "content": response})
    await message.reply(response)