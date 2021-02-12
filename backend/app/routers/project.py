# import asyncio

from hashlib import md5
from typing import Optional

from fastapi import APIRouter, HTTPException
from loguru import logger

from .. import config
from .. import resources as res
from ..models import CodeboxInput, Description, Project, ProjectResponses, Responses

router = APIRouter()


@router.get('/projects/', response_model=list[Project])
async def get_all_projects():
    '''
    Get all example projects on Redis.
    '''

    keys = await res.redis.keys('examples:*')
    projects = await res.redis.mget(*keys)
    return [Project.parse_raw(proj) for proj in projects]


@router.get('/projects/<id>', response_model=Project)
async def get_project(id: int) -> Project:
    project_json = await res.redis.get(f'project:{id}')
    if not project_json:
        raise HTTPException(status_code=404)
    return project_json


@router.put('/projects/<id>')
async def get_project(id: int, description: Description) -> None:
    project_json = await res.redis.get(f'project:{id}')
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
    id = calc_project_id(project_core)
    project_json = await res.redis.get(f'project:{id}')
    if project_json:
        logger.debug(f'Project cached: {project_json}')
        project = Project.parse_raw(project_json)
        prj_responses = ProjectResponses(id=id, responses=project.responses)
        return prj_responses

    # not cached, so run it
    logger.debug(f'Project {id} not cached')
    responses = await run_project_in_container(project_core)

    # cache result
    project = Project(id=id, responses=responses, **project_core)
    save_project(project, config.TIMEOUT)

    # report the result
    prj_responses = ProjectResponses(id=id, responses=responses)
    logger.debug(prj_responses)
    return prj_responses


async def save_project(project: Project, timeout: Optional[int] = None) -> None:
    key = f'project:{project.id}'
    await res.redis.set(key, project.json())
    if timeout:
        await res.redis.expire(key, timeout)


def calc_project_id(proj: CodeboxInput) -> str:
    '''
    Calculates the project id based on its source files, commands and inputs.
    Title and description
    '''
    code = ''.join(f'{s.path}{s.code}' for s in proj.sources)
    commands = ''.join(f'{c.command}{c.input}{c.timeout}' for c in proj.commands)
    text = ''.join([code, commands])
    return md5(text.encode()).hexdigest()


async def run_project_in_container(project: CodeboxInput) -> Responses:
    '''
    Run the project in a sandbox container
    '''
    # use asyncio subprocess here
    logger.debug(project)
    return []
