from fastapi import APIRouter, HTTPException
from loguru import logger

from .. import config
from ..codebox import run_playground_in_codebox
from ..models import PlaygroundInput, PlaygroundOutput, PlaygroundProject, calc_hash
from ..resources import redis

router = APIRouter(prefix='/playgrounds', tags=['playgrounds'])


@router.get('/{id}', response_model=PlaygroundProject)
async def get_playground(id: str) -> PlaygroundProject:
    key = f'playground:{id}'
    data = await redis.get(key)
    if not data:
        # TODO: search database for project
        # if found, cache it
        raise HTTPException(status_code=404)
    return PlaygroundProject.parse_raw(data)


@router.post('', response_model=PlaygroundOutput)
async def run_playground(playground_input: PlaygroundInput) -> PlaygroundOutput:
    """
    Get the execution of the playground code.
    """

    # first, check if the configuration is cached
    id = calc_hash(playground_input)
    key = f'playground:{id}'
    data = await redis.get(key)
    if data:
        logger.info(f'Cached {key}')
        output = PlaygroundOutput.parse_raw(data)
        return output

    # not cached, so run it
    logger.debug(f'{key} not cached')
    responses = await run_playground_in_codebox(playground_input)
    output = PlaygroundOutput(id=id, responses=responses)

    # cache result
    project = PlaygroundProject(**playground_input.dict(), **output.dict())
    await redis.set(key, project.json(), ex=config.TTL)

    # save in the database

    # report the result
    return output
