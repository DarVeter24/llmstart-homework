FROM python:3.11-slim

# Установка uv
RUN pip install uv

# Рабочая директория
WORKDIR /app

# Копирование файлов конфигурации
COPY pyproject.toml ./

# Установка зависимостей
RUN uv sync --frozen

# Копирование исходного кода
COPY . .

# Команда запуска
CMD ["uv", "run", "python", "main.py"]