from unittest.mock import patch

from httpx import AsyncClient
from pydantic import TypeAdapter

from codelab.models import CodelabProject
from codelab.resources import redis


async def test_get_examples(client: AsyncClient) -> None:
    url = '/examples'
    key = 'codelab_examples'

    # first time, there must be no cache
    examples = await redis.get(key)
    assert examples is None

    resp = await client.get(url)
    assert resp.status_code == 200
    assert (await redis.get(key)) == resp.content
    examples = TypeAdapter(list[CodelabProject]).validate_python(resp.json())
    assert len(examples) > 0

    # second call, the project must be in cache
    with patch(
        'codelab.routers.examples.run_codelab_project', return_value=examples
    ) as run_codelab_project:
        resp = await client.get(url)
        assert resp.status_code == 200
        run_codelab_project.assert_not_awaited()
        assert (await redis.get(key)) == resp.content
