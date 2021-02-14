from fastapi import APIRouter, HTTPException
from loguru import logger

from .. import config
from .. import resources as res
from ..models import CodeboxInput, Description, Project, ProjectResponses
from ..projects import calc_id, run_project_in_container, save_project

router = APIRouter()
key = 'project:{}'


@router.get('/projects/{id}', response_model=Project)
async def get_project(id: str) -> Project:
    project_json = await res.redis.get(key.format(id))
    if not project_json:
        raise HTTPException(status_code=404)
    return Project.parse_raw(project_json)


@router.get('/projects', response_model=list[Project])
async def get_all_projects():
    '''
    Get all example projects on Redis.
    '''
    keys = await res.redis.keys(key.format('*'))
    projects = await res.redis.mget(*keys)
    return [Project.parse_raw(proj) for proj in projects]


@router.put('/projects/{id}')
async def update_project(id: str, description: Description) -> None:
    project_json = await res.redis.get(key.format(id))
    if not project_json:
        raise HTTPException(status_code=404)
    project = Project.parse_raw(project_json).copy(update=description.dict())
    await save_project(project)
    return


@router.post('/projects', response_model=ProjectResponses)
async def run_project(project_core: CodeboxInput):
    '''
    Run project if it is not already cached.
    '''

    # first, check if the configuration is cached
    id = calc_id(project_core)
    project_json = await res.redis.get(key.format(id))
    if project_json:
        logger.debug(f'Project cached: {id}')
        project = Project.parse_raw(project_json)
        prj_responses = ProjectResponses(id=id, responses=project.responses)
        return prj_responses

    # not cached, so run it
    logger.debug(f'Project {id} not cached')
    responses = await run_project_in_container(project_core)

    # cache result
    project = Project(**project_core.dict(), id=id, responses=responses)
    await save_project(project, config.TIMEOUT)

    # report the result
    prj_responses = ProjectResponses(id=id, responses=responses)
    logger.debug(prj_responses)
    return prj_responses
