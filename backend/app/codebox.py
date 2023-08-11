from fastapi import HTTPException, status
from httpx import AsyncClient
from loguru import logger
from pydantic import TypeAdapter

from . import config
from .models import (
    CodeboxInput,
    Command,
    PlaygroundInput,
    PlaygroundOutput,
    PlaygroundProject,
    Response,
    calc_hash,
)
from .resources import redis

TIMEOUT = config.TIMEOUT
COMPILATION_TIMEOUT = TIMEOUT * 10
DATABASE_TIMEOUT = TIMEOUT * 10


def playground_to_codebox(project: PlaygroundInput) -> CodeboxInput:
    """
    Call Codebox to run the project
    """
    match project.language.lower():
        case 'python':
            sources = {'main.py': project.sourcecode}
            commands = [
                Command(command='/venv/bin/python main.py', stdin=project.stdin, timeout=TIMEOUT)
            ]

        case 'rust':
            sources = {'main.rs': project.sourcecode}
            commands = [
                Command(command='/usr/local/cargo/bin/rustc main.rs', timeout=COMPILATION_TIMEOUT),
                Command(command='./main', stdin=project.stdin, timeout=TIMEOUT),
            ]

        case 'sqlite' | 'sql' | 'sqlite3':
            sources = {'database.sql': project.sourcecode}
            commands = [
                Command(
                    command='/usr/bin/sqlite3 temp.db -bail -init database.sql ".exit"',
                    timeout=DATABASE_TIMEOUT,
                ),
            ]

        case 'bash':
            sources = {'main.sh': project.sourcecode}
            commands = [
                Command(command='/bin/bash main.sh', stdin=project.stdin, timeout=TIMEOUT),
            ]

        case _:
            raise ValueError(f'Unknown language: {project.language}')

    return CodeboxInput(sources=sources, commands=commands)


async def run_project_in_codebox(project: CodeboxInput) -> list[Response]:
    """
    Call Codebox to run the project
    """
    async with AsyncClient(http2=True, verify=False) as client:  # works like h2c
        response = await client.post(f'{config.CODEBOX_URL}/execute', json=project.model_dump())

    if response.status_code != status.HTTP_200_OK:
        logger.error(f'{response.status_code!r} {response.content!r}')
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    responses = TypeAdapter(list[Response]).validate_python(response.json())
    logger.debug(f'Input: {project!r}, Output: {responses!r}')
    return responses


async def run_playground(playground_input: PlaygroundInput) -> PlaygroundOutput:
    # first, check if the configuration is cached
    id = calc_hash(playground_input)
    key = f'playground:{id}'
    data = await redis.get(key)
    if data:
        logger.info(f'Cached id: {key}')
        return PlaygroundOutput.model_validate_json(data)

    # not cached, so run it
    logger.info(f'id: {key} not cached')
    try:
        codebox_project = playground_to_codebox(playground_input)
    except ValueError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from None
    logger.debug(repr(codebox_project))

    responses = await run_project_in_codebox(codebox_project)
    output = PlaygroundOutput(id=id, responses=responses)

    # cache result
    project = PlaygroundProject(**playground_input.model_dump(), **output.model_dump())
    await redis.set(key, project.model_dump_json(), ex=config.TTL)

    return output
