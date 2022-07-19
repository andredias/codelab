from fastapi import HTTPException
from httpx import AsyncClient
from loguru import logger
from pydantic import parse_obj_as

from . import config
from .models import CodeboxInput, Command, PlaygroundInput, Response


def playground_to_codebox(project: PlaygroundInput) -> CodeboxInput:
    """
    Call Codebox to run the project
    """
    match project.language:
        case 'python':
            sources = {'main.py': project.sourcecode}
            commands = [
                Command(
                    command='/venv/bin/python main.py', stdin=project.stdin
                )
            ]

        case 'rust':
            sources = {'main.rs': project.sourcecode}
            commands = [
                Command(command='/usr/local/cargo/bin/rustc main.rs', timeout=config.TIMEOUT * 10),
                Command(command='./main', stdin=project.stdin),
            ]

        case 'sqlite' | 'sql' | 'sqlite3':
            sources = {'database.sql': project.sourcecode}
            commands = [
                Command(
                    command='/usr/bin/sqlite3 temp.db -bail -init database.sql ".exit"',
                ),
            ]

        case 'bash':
            sources = {'main.sh': project.sourcecode}
            commands = [
                Command(command='/bin/bash main.sh', stdin=project.stdin),
            ]

        case _:
            raise ValueError(f'Unknown language: {project.language}')

    return CodeboxInput(sources=sources, commands=commands)


async def run_project_in_codebox(project: CodeboxInput) -> list[Response]:
    """
    Call Codebox to run the project
    """
    async with AsyncClient() as client:
        response = await client.post(f'{config.CODEBOX_URL}/execute', json=project.dict())

    if response.status_code != 200:
        logger.error(f'{response.status_code!r} {response.content!r}')
        raise HTTPException(500)
    responses = parse_obj_as(list[Response], response.json())
    return responses


async def run_playground_in_codebox(project: PlaygroundInput) -> list[Response]:
    """
    Run the playground project
    """
    try:
        codebox_project = playground_to_codebox(project)
    except ValueError as e:
        raise HTTPException(422, detail=str(e))
    responses = await run_project_in_codebox(codebox_project)
    return responses
