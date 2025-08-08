import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import TELEGRAM_BOT_TOKEN, LOG_LEVEL, validate_config
from bot.handlers import router


async def main():
    """Основная функция запуска бота"""
    # Настройка логирования
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        # Валидация конфигурации
        validate_config()
        logger.info("Configuration validated successfully")
        
        # Инициализация бота и диспетчера
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        dp = Dispatcher()
        
        # Регистрация роутеров
        dp.include_router(router)
        
        # Запуск бота
        logger.info("Starting Telegram bot...")
        await dp.start_polling(bot, allowed_updates=["message"], skip_updates=True)
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return
    finally:
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())