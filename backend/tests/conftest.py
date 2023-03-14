import os
from collections.abc import AsyncIterable, Generator
from pathlib import Path
from subprocess import check_call
from time import sleep

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

os.environ['ENV'] = 'testing'

from app.main import create_app  # noqa: E402


@fixture(scope='session')
def docker() -> Generator:
    root_path = Path(__file__).parent.parent.parent.absolute()
    # fmt: off
    check_call(
        [
            'docker', 'compose',
            '-f', root_path / 'docker-compose.yml',
            '-f', root_path / 'docker-compose.test.yml',
            'up', '-d',
            'redis', 'codebox',
        ]
    )
    # fmt: on
    sleep(2)
    try:
        yield
    finally:
        # fmt: off
        check_call(
            [
                'docker', 'compose',
                '-f', root_path / 'docker-compose.yml',
                '-f', root_path / 'docker-compose.test.yml',
                'down',
            ]
        )
        # fmt: on


@fixture
async def app(docker: Generator) -> AsyncIterable[FastAPI]:
    app = create_app()
    async with LifespanManager(app):
        yield app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(
        app=app,
        base_url='http://testserver',
        headers={'Content-Type': 'application/json'},
    ) as client:
        yield client
