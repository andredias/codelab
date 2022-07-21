from unittest.mock import patch

from httpx import AsyncClient
from pydantic import parse_obj_as

from app.models import PlaygroundProject
from app.resources import redis


async def test_get_examples(client: AsyncClient) -> None:
    url = '/examples'
    key = 'codelab_examples'

    # first time, there must be no cache
    examples = await redis.get(key)
    assert examples is None

    resp = await client.get(url)
    assert resp.status_code == 200
    assert (await redis.get(key)) == resp.content
    examples = parse_obj_as(list[PlaygroundProject], resp.json())
    assert len(examples) > 0

    # second call, the project must be in cache
    with patch('app.routers.examples.run_playground', return_value=examples) as run_playground:
        resp = await client.get(url)
        assert resp.status_code == 200
        run_playground.assert_not_awaited()
        assert (await redis.get(key)) == resp.content
