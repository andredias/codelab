from fastapi import APIRouter, HTTPException

from ..codebox import run_playground
from ..models import PlaygroundInput, PlaygroundOutput, PlaygroundProject
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
async def run_playground_in_codelab(playground_input: PlaygroundInput) -> PlaygroundOutput:
    """
    Get the execution of the playground code.
    """
    output = await run_playground(playground_input)
    return output
