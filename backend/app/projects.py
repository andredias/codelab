from hashlib import md5
from pathlib import Path
from time import time
from typing import Optional

import toml
from httpx import AsyncClient
from loguru import logger
from pydantic import parse_obj_as

from . import config
from .models import CodeboxProject, CodelabProject, Command, ProjectToRun, Response
from .resources import redis


async def save_project(project: CodelabProject, ttl: Optional[int] = None, key: str = 'project:{}') -> None:
    '''
    Save project into Redis
    '''
    key = key.format(project.id)
    await redis.set(key, project.json(), ex=ttl)
    logger.info(f'Key: {key}, TTL: {ttl}s, {project}')
    return


def calc_id(proj: ProjectToRun) -> str:
    '''
    Calculates the project id based on the MD5 of its title, description, source code,
    language and inputs. The order matters.
    '''
    text = ''.join([proj.title, proj.description, proj.language, proj.sourcecode, str(proj.stdin)])
    return md5(text.encode()).hexdigest()


def codelab_to_codebox_project(project: ProjectToRun) -> CodeboxProject:
    language_mappings = {
        'python': {
            'filename': 'main.py',
            'command': '/usr/local/bin/python main.py'
        },
    }
    mapping = language_mappings[project.language]
    sources = {
        mapping['filename']: project.sourcecode,
    }
    cmd = Command(command=mapping['command'], timeout=config.TIMEOUT, stdin=project.stdin)
    return CodeboxProject(sources=sources, commands=[cmd])


async def run_project_in_codebox(project: ProjectToRun) -> Response:
    '''
    Call Codebox to run the project
    '''
    start = time()
    codebox_project = codelab_to_codebox_project(project)
    async with AsyncClient() as client:
        result = await client.post(f'{config.CODEBOX_URL}/execute', json=codebox_project.dict())

    assert result.status_code == 200
    elapsed = time() - start
    logger.debug(f'Elapsed Time: {elapsed}s')
    responses = parse_obj_as(list[Response], result.json())
    return responses[0]


async def load_examples() -> list[CodelabProject]:
    '''
    Load examples into Redis.
    Examples/Samples are the toml files located at 'app/examples'.
    '''
    examples = []
    for example in (Path(__file__).parent / 'examples').glob('*.toml'):
        project = CodelabProject.parse_obj(toml.loads(example.read_text()))
        await save_project(project)
        examples.append(project)
    return examples
