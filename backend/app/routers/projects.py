from fastapi import APIRouter, HTTPException
from loguru import logger

from .. import config
from .. import resources as res
from ..models import CodelabProject, ProjectResponse, ProjectToRun
from ..projects import calc_id, run_project_in_codebox, save_project

router = APIRouter()


@router.get('/projects/{id}', response_model=CodelabProject)
async def get_project(id: str) -> CodelabProject:
    project_json = await res.redis.get(f'project:{id}')
    if not project_json:
        raise HTTPException(status_code=404)
    return CodelabProject.parse_raw(project_json)


@router.get('/projects', response_model=list[CodelabProject])
async def get_all_projects():
    '''
    Get all projects on Redis
    '''
    # TODO: get only most recent projects
    keys = await res.redis.keys('project:*')
    if len(keys) == 0:
        return []
    projects_json = await res.redis.mget(*keys)
    projects = [CodelabProject.parse_raw(proj) for proj in projects_json]
    return projects


@router.post('/projects', response_model=ProjectResponse)
async def run_project(project: ProjectToRun):
    '''
    Run project if it is not already cached.
    '''

    # first, check if the configuration is cached
    id = calc_id(project)
    project_json = await res.redis.get(f'project:{id}')
    if project_json:
        logger.info(f'Project cached: {id}')
        return ProjectResponse.parse_raw(project_json)

    # not cached, so run it
    logger.debug(f'Project {id} not cached')
    response = await run_project_in_codebox(project)

    # cache result
    codelab_project = CodelabProject(**project.dict(), id=id, **response.dict())
    await save_project(codelab_project, config.TTL)

    # report the result
    return ProjectResponse(id=id, **response.dict())
