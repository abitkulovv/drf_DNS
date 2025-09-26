FROM python:3.13-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y curl build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /app
WORKDIR /app

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

