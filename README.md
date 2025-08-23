## 📦 Технологии

- **DDD-архитектура**
- **Python 3.10+**
- **FastAPI** — REST API
- **SQLAlchemy (async)** — ORM
- **Alembic** — миграции БД
- **Pydantic** — DTO и валидация
- **PostgreSQL** / SQLite (для dev)
- **Poetry** — управление зависимостями
---


## env example

```commandline
DATABASE_URL=postgresql+asyncpg://postgres:123@localhost:5433/test_db
HOST=127.0.0.1
PORT=8000
SECRET_KEY=3b3f9a48155374edd9981b0a574b269b9bc6f59318c721733137e52d3969c0c999e94f46991296c6925482f544be272c
ALGORITHM=HS256
```
---
## ⚙️ Установка

```bash
# Instal dependencies
poetry install
# Initiate pre-commit
poetry run pre-commit install
```

---


## 🗃️ Миграции

```bash
poetry run alembic revision --autogenerate -m "Revision Name"
poetry run alembic upgrade head
```

---

## 🧭 Тесты

```bash
poetry run pytest -vv
```
---


## 🚀 Запуск

```bash
bash docker-entrypoint.sh
```

Открой Swagger UI:
```
http://localhost:8000/docs
```

---