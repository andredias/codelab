from hashlib import md5
from pathlib import Path
from time import time

import toml
from httpx import AsyncClient
from loguru import logger
from pydantic import parse_obj_as

from . import config
from . import resources as res
from .models import Project, ProjectCore, ProjectDescriptionCore, Response


async def save_project(project: Project, ttl: int = 0, key: str = 'project:{}') -> None:
    '''
    Save project into Redis
    '''
    key = key.format(project.id)
    await res.redis.set(key, project.json(), expire=ttl)
    logger.info(f'Key: {key}, TTL: {ttl}s, {project}')
    return


def calc_id(proj: ProjectDescriptionCore) -> str:
    '''
    Calculates the project id based on the MD5 of its title, description, source files, commands and inputs.
    The order matters.
    '''
    code = ''.join(f'{path}{code}' for path, code in sorted(proj.sources.items()))
    commands = ''.join(f'{c.command}{c.stdin}{c.timeout}' for c in proj.commands)
    text = ''.join([proj.title, proj.description, code, commands])
    return md5(text.encode()).hexdigest()


async def run_project_in_codebox(project_core: ProjectCore) -> list[Response]:
    '''
    Call Codebox to run the project
    '''
    start = time()

    async with AsyncClient() as client:
        result = await client.post(f'{config.CODEBOX_URL}/execute', json=project_core.dict())

    assert result.status_code == 200
    elapsed = time() - start
    logger.debug(f'Elapsed Time: {elapsed}s')
    return parse_obj_as(list[Response], result.json())


async def load_examples() -> list[Project]:
    '''
    Load examples into Redis.
    Examples/Samples are the toml files located at 'app/examples'.
    '''
    examples = []
    for example in (Path(__file__).parent / 'examples').glob('*.toml'):
        project = Project.parse_obj(toml.loads(example.read_text()))
        await save_project(project)
        examples.append(project)
    return examples
