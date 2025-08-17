# README.md

Асинхронный backend (FastAPI + SQLAlchemy async + asyncpg + PostgreSQL). Эмулирует приём платежей через webhook, хранит Users, Admins, Accounts (balance) и Transactions.

## Перед использованием создать `.env` по `.env.exmaple`

## Запуск (Docker Compose)

```bash
# собрать и поднять БД + приложение
docker compose up --build -d

# запустить миграции
docker compose exec app alembic upgrade head

# создать таблицы и сиды (тестовые данные)
docker compose exec app python -m src.seed
```

## Запуск локально (без Docker)

```bash
# подготовка
python -m venv .venv
source .venv/bin/activate    
pip install -r requirements.txt

# создать таблицы и сиды
python -m src.seed

# запустить приложение
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Тестовые данные (создаются скриптом `src/seed.py`)

* Пользователь: `test@example.com` / `testpass` — у него будет создан тестовый Account
* Администратор: `admin@example.com` / `adminpass`

