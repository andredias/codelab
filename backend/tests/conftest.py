import os
from collections.abc import AsyncIterable, Generator
from subprocess import DEVNULL, check_call
from time import sleep

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

from app import create_app  # isort:skip
from app import config  # isort:skip

os.environ['ENV'] = 'testing'
os.environ['REDIS_URL'] = 'redis://localhost:6378'
os.environ['TIMEOUT'] = '1'
config.init()


@fixture(scope='session')
def docker() -> Generator:
    codebox_port = config.CODEBOX_URL.split(':')[-1]
    redis_port = config.REDIS_URL.split(':')[-1]
    check_call(
        f'docker run -d --privileged --rm -p {codebox_port}:8000 --name codebox-testing codebox',
        stdout=DEVNULL,
        shell=True
    )
    check_call(f'docker run -d --rm -p {redis_port}:6379 --name redis-testing redis:alpine', stdout=DEVNULL, shell=True)
    sleep(1)
    try:
        yield
    finally:
        check_call('docker stop -t 0 codebox-testing redis-testing', stdout=DEVNULL, shell=True)


@fixture
async def app(docker) -> AsyncIterable[FastAPI]:  # noqa: F811
    app = create_app()
    async with LifespanManager(app):
        yield app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
