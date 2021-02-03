from httpx import AsyncClient
from loguru import logger

from app.models import ProjectIn  # isort:skip


async def test_run_project(client: AsyncClient) -> None:
    message = 'Hello World!'
    project = ProjectIn(
        sources=[
            dict(path='main.py', code=f'print("{message}")\n')
        ],
        run_command='python main.py',
        title='Hello World',
    )
    logger.info(project)
    resp = await client.post('/projects', json=project.dict())
    assert resp.status_code == 200
    data = resp.json()
    assert len(data['id']) == 32
    assert data['output']['stdout'] == message
    assert 'stderr' not in data['output'].keys()
