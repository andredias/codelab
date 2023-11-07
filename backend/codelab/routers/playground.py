from fastapi import APIRouter, HTTPException
from loguru import logger

from ..codebox import run_codelab_project
from ..models import CodelabInput, CodelabOutput, CodelabProject
from ..resources import redis

router = APIRouter(prefix='/playgrounds', tags=['playgrounds'])


@router.get('/{id}', response_model=CodelabProject)
async def get_codelab_project(id: str) -> CodelabProject:
    """
    Get a playground project
    """
    key = f'codelab:{id}'
    data = await redis.get(key)
    if not data:
        # TODO: search database for project
        # if found, cache it
        logger.info(f'{id} Not found')
        raise HTTPException(status_code=404)
    project = CodelabProject.model_validate_json(data)
    logger.info(project.model_dump_json())
    return project


@router.post('', response_model=CodelabOutput)
async def exec_codelab_project(codelab_input: CodelabInput) -> CodelabOutput:
    """
    Execute a playground input
    """
    output = await run_codelab_project(codelab_input)
    logger.info(
        CodelabProject(**codelab_input.model_dump(), **output.model_dump()).model_dump_json()
    )
    return output
