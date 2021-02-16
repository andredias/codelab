from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from hashlib import md5
from pathlib import Path
from time import time
from typing import Optional

import aiofiles
import toml
from loguru import logger
from pydantic import parse_raw_as

from . import resources as res
from .models import CodeboxInput, Command, Project, Response


async def save_project(project: Project, timeout: Optional[int] = 0) -> None:
    key = f'project:{project.id}'
    await res.redis.set(key, project.json(), expire=timeout)
    logger.debug(f'{key}, {project}')
    return


def calc_id(proj: CodeboxInput) -> str:
    '''
    Calculates the project id based on its source files, commands and inputs.
    Title and description
    '''
    code = ''.join(f'{path}{code}' for path, code in proj.sources.items())
    commands = ''.join(f'{c.command}{c.input}{c.timeout}' for c in proj.commands)
    text = ''.join([code, commands])
    return md5(text.encode()).hexdigest()


async def run_project_in_container(project_core: CodeboxInput) -> list[Response]:
    '''
    Run the project in a sandbox container
    '''
    start = time()

    project_json = project_core.json().encode()
    docker_cmd = ['docker', 'run', '-i', '--rm', 'codebox']
    proc = await create_subprocess_exec(*docker_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate(input=project_json)
    assert stderr == b''
    result = parse_raw_as(list[Response], stdout)

    elapsed = time() - start
    logger.debug(f'elapsed time: {elapsed}')
    return result


async def load_examples() -> None:
    '''
    Load examples into Redis
    '''
    for example in (Path(__file__).parent / 'examples').glob('*.toml'):
        project = Project.parse_obj(toml.loads(example.read_text()))
        await save_project(project)
