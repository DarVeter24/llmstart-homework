FROM python:3.11-slim

# Установка uv
RUN pip install --no-cache-dir uv

# Рабочая директория
WORKDIR /app

# Копирование файлов конфигурации зависимостей
COPY pyproject.toml uv.lock ./

# Установка зависимостей по lock-файлу
RUN uv sync --frozen

# Копирование исходного кода
COPY . .

# Команда запуска
CMD ["uv", "run", "python", "main.py"]