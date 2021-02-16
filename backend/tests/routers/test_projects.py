from time import sleep
from unittest.mock import patch

from httpx import AsyncClient
from loguru import logger

from app import config  # isort:skip
from app.models import Command, Project, ProjectDescriptionCore  # isort:skip


async def test_run_project(client: AsyncClient) -> None:
    project = ProjectDescriptionCore(
        sources={'main.py': 'print("Hello World!")\n'},
        commands=[Command(command='python main.py', timeout=0.1)],
        title='Hello World',
        description='Classic first project',
    )
    logger.info('project not in cache')
    resp = await client.post('/projects', json=project.dict())
    assert resp.status_code == 200
    data = resp.json()
    assert data == {
        'id': 'b5cd234f6bda2e78b149966dc528dde9',
        'responses': [{
            'stdout': 'Hello World!\n',
            'stderr': '',
            'exit_code': 0
        }]
    }

    # second call, the project must be in cache
    with patch(
        'app.routers.projects.run_project_in_container', return_value=data['responses']
    ) as run_project_in_container:
        logger.info('project must be in cache')
        resp = await client.post('/projects', json=project.dict())
        assert resp.status_code == 200
        run_project_in_container.assert_not_awaited()

        # third call: not in cache anymore, must call run_project_in_container
        logger.debug('sleeping...')
        sleep(config.TIMEOUT + 1)
        logger.info('project must not be in cache anymore')
        resp = await client.post('/projects', json=project.dict())
        assert resp.status_code == 200
        run_project_in_container.assert_awaited()


async def test_get_all_projects(examples: list[Project], client: AsyncClient) -> None:
    resp = await client.get('/projects')
    assert len(resp.json()) == len(examples)


async def test_get_project(examples: list[Project], client: AsyncClient) -> None:
    resp = await client.get(f'/projects/{examples[0].id}')
    assert resp.status_code == 200
    project = Project.parse_obj(resp.json())
    assert project.title == examples[0].title

    resp = await client.get('/projects/00000000000000000000000000000001')
    assert resp.status_code == 404
