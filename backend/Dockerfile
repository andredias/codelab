FROM python:3.13.0a4-slim as builder
LABEL maintainer="André Felipe Dias <andref.dias@gmail.com>"

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN python -m venv /venv

ENV POETRY_VERSION=1.5.1
ENV POETRY_HOME=/opt/poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate; \
    $POETRY_HOME/bin/poetry install --only main --no-interaction


FROM python:3.13.0a4-slim as final

COPY --from=builder /venv /venv
ENV PATH=/venv/bin:${PATH}

WORKDIR /app
USER nobody
COPY --chown=nobody:nogroup hypercorn.toml .
COPY --chown=nobody:nogroup codelab/ ./codelab

CMD ["hypercorn", "--config=hypercorn.toml", "codelab.main:app"]
