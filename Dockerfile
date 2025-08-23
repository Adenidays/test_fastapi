FROM python:3.12.0-slim-bullseye AS python-base

# Environ
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="${PATH}:/root/.local/bin" \
    POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_CACHE_DIR=/opt/.cache

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN apt-get update
RUN apt-get -y install make

FROM python-base AS poetry-base

RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install poetry

FROM python-base AS project8-api

ARG APP_USER=project8
ARG WORK_DIR=/app

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR ${WORK_DIR}

COPY . ${WORK_DIR}

RUN poetry install --no-interaction --no-cache

EXPOSE 8000

RUN groupadd \
    --system ${APP_USER} \
    && useradd --no-log-init --system --gid ${APP_USER} ${APP_USER}

USER ${APP_USER}:${APP_USER}

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
