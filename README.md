# LLM Start — Telegram LLM Assistant

Минимальный Телеграм‑бот‑консультант на LLM. Реализован по принципу KISS и в 5 итераций (см. `doc/tasklist.md`, `doc/vision.md`).

## Возможности
- Ответы ИИ на вопросы пользователей (OpenRouter через OpenAI client)
- Контекстный диалог с историей (in‑memory)
- Сценарии: приветствие/знакомство, список услуг `/services`
- Логирование запросов/ответов LLM

## Стек
- Python 3.11+, aiogram 3
- OpenRouter (OpenAI SDK)
- uv, pytest, make, Docker

## Конфигурация
Создайте `.env` в корне:

```
TELEGRAM_BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxxxxxx

# Опционально (есть значения по умолчанию)
LLM_MODEL=anthropic/claude-3.5-sonnet
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=500
LOG_LEVEL=INFO
SYSTEM_PROMPT=Вы дружелюбный и полезный ассистент. Отвечайте кратко, по делу и на русском языке.
MAX_HISTORY_MESSAGES=10
OPENROUTER_HTTP_REFERER=
OPENROUTER_APP_TITLE=LLMStartBot
```

## Быстрый старт (локально)
```
make dev           # установить зависимости для разработки
make check-config  # проверить конфиг
make run           # запустить бота
make stop          # остановить бота
make test          # запустить тесты
```

Команды бота в Telegram: `/start`, `/help`, `/services`.

## Запуск в Docker
```
make docker-build
make docker-run     # использует .env
docker logs -f llmstart-bot
make docker-stop
```

## Полезное
- Документация и план: `doc/vision.md`, `doc/tasklist.md`, `doc/guides/botfather.md`
- Известная причина ошибок LLM: 401 Unauthorized — проверьте корректный серверный ключ OpenRouter (`sk-or-...`)

## Статус
✅ Завершено (итерации 1–5 выполнены)