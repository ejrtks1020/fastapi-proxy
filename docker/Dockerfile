FROM python:3.11.6-slim AS builder

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY proxy_server/pyproject.toml proxy_server/poetry.lock /app/

WORKDIR /app

RUN apt-get update --fix-missing
RUN apt-get install -y default-libmysqlclient-dev pkg-config gcc g++
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --only main --no-root

FROM python:3.11.6-slim AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update --fix-missing
RUN apt-get install -y software-properties-common net-tools curl procps supervisor vim default-libmysqlclient-dev pkg-config
WORKDIR /app
COPY proxy_server/ /app
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY proxy_server/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord", "-n"]
