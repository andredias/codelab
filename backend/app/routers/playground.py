from fastapi import APIRouter, HTTPException
from loguru import logger

from ..codebox import run_playground
from ..models import PlaygroundInput, PlaygroundOutput, PlaygroundProject
from ..resources import redis

router = APIRouter(prefix='/playgrounds', tags=['playgrounds'])


@router.get('/{id}', response_model=PlaygroundProject)
async def get_playground(id: str) -> PlaygroundProject:
    """
    Get a playground project
    """
    key = f'playground:{id}'
    data = await redis.get(key)
    if not data:
        # TODO: search database for project
        # if found, cache it
        logger.info(f'{id} Not found')
        raise HTTPException(status_code=404)
    project = PlaygroundProject.model_validate_json(data)
    logger.info(project.model_dump_json())
    return project


@router.post('', response_model=PlaygroundOutput)
async def run_playground_in_codelab(playground_input: PlaygroundInput) -> PlaygroundOutput:
    """
    Execute a playground input
    """
    output = await run_playground(playground_input)
    logger.info(
        PlaygroundProject(**playground_input.model_dump(), **output.model_dump()).model_dump_json()
    )
    return output
