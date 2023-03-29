FROM python:3.10-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev libxml2-dev \
    libxslt-dev curl libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV POETRY_VERSION=1.4.1
RUN curl https://install.python-poetry.org | python -

RUN python -m venv /venv
ENV PATH=/venv/bin:/root/.local/bin:${PATH}

WORKDIR /codelab
COPY pyproject.toml poetry.lock ./

RUN . /venv/bin/activate; \
    poetry install --only main --no-interaction

FROM python:3.10-slim as final

COPY --chown=nobody:nogroup --from=builder /venv /venv
ENV PATH=/venv/bin:${PATH}

WORKDIR /codelab
RUN chown -R nobody:nogroup .
COPY --chown=nobody:nogroup app ./app
COPY --chown=nobody:nogroup hypercorn.toml .
COPY --chown=nobody:nogroup self-signed.* .

# USER nobody

EXPOSE 5000
CMD ["hypercorn", "--config=hypercorn.toml", "--keyfile=self-signed.key", \
    "--certfile=self-signed.crt", "--root-path=/api", "app.main:app"]
