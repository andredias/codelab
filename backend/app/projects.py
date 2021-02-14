import json
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from hashlib import md5
from pathlib import Path
from typing import Optional

import aiofiles
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
    project_json = project_core.json().encode()
    docker_cmd = ['docker', 'run', '-i', '--rm', 'codebox']
    proc = await create_subprocess_exec(*docker_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate(input=project_json)
    assert stderr == b''
    return parse_raw_as(list[Response], stdout)


async def run_examples() -> list[Project]:
    examples_dir = Path(__file__).parent / 'examples'
    python_examples = examples_dir.glob('*.py')  # only Python so far
    examples = []
    for program in python_examples:
        command = Command(command=f'python {program.name}', timeout=0.1)
        async with aiofiles.open(program) as f:
            source_code = await f.read()
        core = CodeboxInput(sources={program.name: source_code}, commands=[command])
        id = calc_id(core)
        responses = await run_project_in_container(core)
        project = Project(id=id, responses=responses, **core.dict())
        examples.append(project)
        logger.debug(json.dumps(project.dict(), ensure_ascii=False, indent=4))
    return examples
