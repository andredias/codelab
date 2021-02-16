import os
from collections.abc import AsyncIterable, Generator
from pathlib import Path
from subprocess import DEVNULL, check_call

import aiofiles
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import parse_raw_as
from pytest import fixture

from app import create_app  # isort:skip
from app import config  # isort:skip
from app.models import Project  # isort:skip
from app.projects import save_project  # isort:skip

os.environ['ENV'] = 'testing'
os.environ['REDIS_URL'] = 'redis://localhost:6378'
os.environ['TIMEOUT'] = '1'
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
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@fixture
async def examples(app: AsyncIterable[FastAPI]) -> list[Project]:
    async with aiofiles.open(Path(__file__).parent.parent / 'app/examples/projects.json') as f:
        examples_json = await f.read()
    projects = parse_raw_as(list[Project], examples_json)
    for project in projects:
        await save_project(project)
    return projects