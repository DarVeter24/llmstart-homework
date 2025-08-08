.PHONY: install test run stop clean dev

# Установка зависимостей через uv
install:
	uv sync

# Установка зависимостей для разработки
dev:
	uv sync --extra dev

# Запуск тестов
test:
	uv run pytest tests/ -v

# Запуск бота
run:
	uv run python main.py

# Остановка бота
stop:
	@./stop_bot.sh

# Очистка временных файлов
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

# Проверка конфигурации
check-config:
	@echo "Checking configuration..."
	@if [ ! -f .env ]; then echo "Warning: .env file not found. Copy from env.example"; fi
	@uv run python -c "from config import validate_config; validate_config(); print('Configuration is valid')"

# Помощь
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies with uv"
	@echo "  dev         - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  run         - Run the bot"
	@echo "  stop        - Stop the bot"
	@echo "  clean       - Clean temporary files"
	@echo "  check-config - Check configuration"