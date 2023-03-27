import os
from collections.abc import AsyncIterable

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

os.environ['ENV'] = 'testing'

from app.main import create_app  # noqa: E402


@fixture
async def app() -> AsyncIterable[FastAPI]:
    app = create_app()
    async with LifespanManager(app):
        yield app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
