from fastapi import APIRouter, HTTPException
from loguru import logger

from .. import config
from .. import resources as res
from ..models import Project, ProjectCore, ProjectDescriptionCore, ProjectResponses
from ..projects import calc_id, run_project_in_container, save_project

router = APIRouter()


@router.get('/projects/{id}', response_model=Project)
async def get_project(id: str) -> Project:
    project_json = await res.redis.get(f'project:{id}')
    if not project_json:
        raise HTTPException(status_code=404)
    return Project.parse_raw(project_json)


@router.get('/projects', response_model=list[Project])
async def get_all_projects():
    '''
    Get all projects on Redis
    '''
    # TODO: get only most recent projects
    keys = await res.redis.keys('project:*')
    if len(keys) == 0:
        return []
    projects_json = await res.redis.mget(*keys)
    projects = [Project.parse_raw(proj) for proj in projects_json]
    return projects


@router.post('/projects', response_model=ProjectResponses)
async def run_project(description_core: ProjectDescriptionCore):
    '''
    Run project if it is not already cached.
    '''
    # ensures that timeout is 0.1 max for non-authenticated projects
    # This prevents direct access via API to run long processes
    for command in description_core.commands:
        command.timeout = config.TIMEOUT
    # first, check if the configuration is cached
    id = calc_id(description_core)
    project_json = await res.redis.get(f'project:{id}')
    if project_json:
        logger.debug(f'Project cached: {id}')
        project = Project.parse_raw(project_json)
        return ProjectResponses(id=project.id, responses=project.responses)

    # not cached, so run it
    logger.debug(f'Project {id} not cached')
    responses = await run_project_in_container(ProjectCore(**description_core.dict()))

    # cache result
    project = Project(**description_core.dict(), id=id, responses=responses)
    await save_project(project, config.TTL)

    # report the result
    prj_responses = ProjectResponses(id=id, responses=responses)
    return prj_responses
