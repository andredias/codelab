from time import sleep
from unittest.mock import patch

from httpx import AsyncClient
from loguru import logger

from app import config
from app.models import CodelabProject, ProjectToRun, Response


async def test_run_project(client: AsyncClient) -> None:
    project = ProjectToRun(
        sourcecode='print("Hello World!")\n',
        language='python',
        title='Hello World',
        description='Classic first project',
    )
    logger.info('project not in cache')
    resp = await client.post('/projects', json=project.dict())
    assert resp.status_code == 200
    data = resp.json()
    assert data['id'] == '7ded54706f0aefbd641bbbe452ecb174'
    assert Response(**data) == Response(
        stdout='Hello World!\n',
        stderr='',
        exit_code=0,
    )

    # second call, the project must be in cache
    with patch(
        'app.routers.projects.run_project_in_codebox', return_value=Response(**data)
    ) as run_project_in_codebox:
        logger.info('project must be in cache')
        resp = await client.post('/projects', json=project.dict())
        assert resp.status_code == 200
        run_project_in_codebox.assert_not_awaited()

        # third call: not in cache anymore, must call run_project_in_codebox
        logger.debug('sleeping...')
        sleep(config.TIMEOUT + config.TTL)
        logger.info('project must not be in cache anymore')
        resp = await client.post('/projects', json=project.dict())
        assert resp.status_code == 200
        run_project_in_codebox.assert_awaited()


async def test_get_all_projects(client: AsyncClient) -> None:
    """
    Examples must have been loaded automatically
    """
    resp = await client.get('/projects')
    assert len(resp.json()) > 0


async def test_get_project(client: AsyncClient) -> None:
    example = (await client.get('/projects')).json()[0]

    resp = await client.get(f'/projects/{example["id"]}')
    assert resp.status_code == 200
    project = CodelabProject.parse_obj(resp.json())
    assert project.title == example['title']

    resp = await client.get('/projects/00000000000000000000000000000001')
    assert resp.status_code == 404
