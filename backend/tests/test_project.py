from httpx import AsyncClient
from loguru import logger

from app.models import ProjectIn  # isort:skip
from app.routers.project import calc_project_id  # isort:skip


async def test_calc_project_id():
    message = 'Hello World!'
    proj1 = ProjectIn(
        sources=[dict(path='main.py', code=f'print("{message}")\n')],
        commands=[dict(command='python main.py', timeout=0.1)],
        title='Hello World',
    )
    proj2 = ProjectIn(
        sources=[dict(path='source.py', code=f'print("{message}")\n')],
        commands=[dict(command='python main.py', timeout=0.1)],
        title='Hello World',
    )

    id_proj1 = calc_project_id(proj1)
    id_proj2 = calc_project_id(proj2)

    assert len(id_proj1) == len(id_proj2) == 32
    assert id_proj1 != id_proj2
    assert calc_project_id(proj1) == calc_project_id(proj1)


async def test_run_project(client: AsyncClient) -> None:
    message = 'Hello World!'
    project = ProjectIn(
        sources=[dict(path='main.py', code=f'print("{message}")\n')],
        commands=[dict(command='python main.py', timeout=0.1)],
        title='Hello World',
    )
    logger.info(project)
    resp = await client.post('/projects', json=project.dict())
    assert resp.status_code == 200
    data = resp.json()
    assert data['output']['stdout'] == message
    assert 'stderr' not in data['output'].keys()
