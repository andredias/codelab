from time import sleep
from unittest.mock import patch

from httpx import AsyncClient

from app import config
from app.models import PlaygroundInput, PlaygroundOutput, Response

project = PlaygroundInput(
    sourcecode='print("Hello World!")\n',
    language='python',
)


async def test_run_project(client: AsyncClient) -> None:

    # project not in cache
    resp = await client.post('/playgrounds', json=project.dict())
    assert resp.status_code == 200
    data = resp.json()
    output = PlaygroundOutput(**data)
    assert output == PlaygroundOutput(
        id='inMUAUBBwpoHwVB7UQ5OXQ',
        responses=[
            Response(
                stdout='Hello World!\n',
                stderr='',
                exit_code=0,
            ),
        ],
    )

    # second call, the project must be in cache
    with patch(
        'app.codebox.run_project_in_codebox', return_value=output.responses
    ) as run_project_in_codebox:
        resp = await client.post('/playgrounds', json=project.dict())
        assert resp.status_code == 200
        run_project_in_codebox.assert_not_awaited()

        # third call: not in cache anymore, must call run_project_in_codebox
        sleep(config.TIMEOUT + config.TTL)
        resp = await client.post('/playgrounds', json=project.dict())
        assert resp.status_code == 200
        run_project_in_codebox.assert_awaited()


async def test_non_existent_language(client: AsyncClient) -> None:
    project = PlaygroundInput(sourcecode='tra-la-la', language='something else', stdin='')
    resp = await client.post('/playgrounds', json=project.dict())
    assert resp.status_code == 422


async def test_get_playground(client: AsyncClient) -> None:
    resp = await client.get('/playgrounds/nonexistent-id')
    assert resp.status_code == 404

    # insert a project in cache
    resp = await client.post('/playgrounds', json=project.dict())
    assert resp.status_code == 200
    data = resp.json()
    id = data['id']
    resp = await client.get(f'/playgrounds/{id}')
    assert resp.status_code == 200
    assert resp.json() == (data | project.dict() | {'title': ''})
