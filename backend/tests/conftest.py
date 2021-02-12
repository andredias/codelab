from collections.abc import AsyncIterable, Generator
from pathlib import Path
from subprocess import DEVNULL, check_call

from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from fastapi import FastAPI
from httpx import AsyncClient
from loguru import logger
from pytest import fixture

from app import create_app  # isort:skip
from app import config  # isort:skip
from app import resources as res  # isort:skip

load_dotenv(Path(__file__).parent / 'env')
config.init()


@fixture(scope='session')
def docker() -> Generator:
    redis_port = config.REDIS_URL.split(':')[-1]
    check_call(f'docker run -d --rm -p {redis_port}:6379 --name redis-testing redis:alpine', stdout=DEVNULL, shell=True)
    try:
        yield
    finally:
        check_call('docker stop -t 0 redis-testing', stdout=DEVNULL, shell=True)


@fixture
async def app(docker) -> AsyncIterable[FastAPI]:  # noqa: F811
    app = create_app()
    async with LifespanManager(app):
        yield app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    await res.redis.flushdb()  # clean redis database everytime
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
