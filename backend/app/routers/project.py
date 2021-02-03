# import asyncio

from hashlib import md5
from typing import List

from fastapi import APIRouter, HTTPException
from loguru import logger

from .. import config
from .. import resources as res
from ..models import Output, Project, ProjectCore, ProjectIn, ProjectOut

router = APIRouter()


@router.get('/projects/examples', response_model=List[Project])
async def get_all_projects():
    '''
    Get all example projects on Redis.
    '''

    keys = await res.redis.keys('examples:*')
    projects = await res.redis.mget(*keys)
    return [Project.parse_raw(proj) for proj in projects]


@router.get('/projects/<id>', response_model=Project)
async def get_project(id: int) -> Project:
    project = await res.redis.get(f'project:{id}')
    if not project:
        raise HTTPException(status_code=404)
    return project


@router.post('/projects',
             response_model=ProjectOut,
             response_model_exclude_none=True)
async def run_project(project: ProjectIn):
    # first, check if the configuration is cached
    id = calc_project_id(project)
    project_json = await res.redis.get(f'project:{id}')
    if project_json:
        logger.debug(f'Project cached: {project_json}')
        project = Project.parse_raw(project_json)
        return ProjectOut(**project.dict(), id=id)

    # not cached, so run it
    logger.debug(f'Project {id} not cached')
    proj_core = ProjectCore(**project.dict())
    output = await run_project_in_container(proj_core)

    # cache result
    project_to_cache = Project(**project.dict(), id=id, output=output)
    key = f'project:{id}'
    await res.redis.set(key, project_to_cache.json())
    await res.redis.expire(key, config.TIMEOUT)

    # report the result
    response = ProjectOut(id=id, output=output)
    logger.debug(response)
    return response


def calc_project_id(proj: ProjectCore) -> str:
    code = ''.join(f'{s.path}{s.code}' for s in proj.sources)
    commands = ''.join(c.command for c in proj.commands)
    text = ''.join(
        [code, commands, proj.input])
    return md5(text.encode()).hexdigest()


async def run_project_in_container(project: ProjectCore) -> Output:
    '''
    Run the project in a sandbox container
    '''
    # use asyncio subprocess here
    logger.debug(project)
    output = Output(stdout='Hello World!')
    return output
