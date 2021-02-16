from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from hashlib import md5
from pathlib import Path
from time import time

import toml
from loguru import logger
from pydantic import parse_raw_as

from . import resources as res
from .models import Project, ProjectCore, ProjectDescriptionCore, Response


async def save_project(project: Project, timeout: int = 0, key: str = 'project:{}') -> None:
    '''
    Save project into Redis

    Different keys might be used. Examples might use 'example:{}' as their key pattern, for example.
    Even if projects have the same ID, they might be in different keys.
    '''
    key = key.format(project.id)
    await res.redis.set(key, project.json(), expire=timeout)
    logger.debug(f'{key}, {project}')
    return


def calc_id(proj: ProjectDescriptionCore) -> str:
    '''
    Calculates the project id based on the MD5 of its title, description, source files, commands and inputs.
    The order matters.
    '''
    code = ''.join(f'{path}{code}' for path, code in proj.sources.items())
    commands = ''.join(f'{c.command}{c.input}{c.timeout}' for c in proj.commands)
    text = ''.join([proj.title, proj.description, code, commands])
    return md5(text.encode()).hexdigest()


async def run_project_in_container(project_core: ProjectCore) -> list[Response]:
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
    logger.debug(f'Elapsed Time: {elapsed}s')
    return result


async def load_examples() -> None:
    '''
    Load examples into Redis.
    Examples/Samples are the toml files located at 'app/examples'.

    Examples are saved twice in Redis. Under 'example:{id}' and 'project:{id}' keys.
    The 'example:{}' key is used to differentiate examples from ordinary projects.
    Thus, we can select only examples instead of all projects.
    The 'project:{}' key is used to retrieve an example as any ordinary project
    by the /projects/{id} route.
    '''
    for example in (Path(__file__).parent / 'examples').glob('*.toml'):
        project = Project.parse_obj(toml.loads(example.read_text()))
        await save_project(project, key='example:{}')
        await save_project(project)  # saved also under 'project:{id}' key


async def get_examples() -> list[Project]:
    '''
    Retrieve all projects that are proposed as examples by default.
    The examples are registered in TOML files at app/examples.
    '''
    keys = await res.redis.keys('example:*')
    if len(keys) == 0:  # examples weren't loaded
        await load_examples()
        keys = await res.redis.keys('example:*')
        assert keys
    examples = await res.redis.mget(*keys)
    projects = [Project.parse_raw(proj) for proj in examples]
    return projects
