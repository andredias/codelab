import asyncio
from pathlib import Path
from unittest.mock import patch

import orjson
import tomli
from fastapi import APIRouter
from loguru import logger
from pydantic import TypeAdapter

from .. import config
from ..codebox import run_playground
from ..models import PlaygroundInput, PlaygroundProject
from ..resources import redis

router = APIRouter(prefix='/examples', tags=['examples'])


async def run_example(
    title: str, language: str, sourcecode: str, stdin: str = ''
) -> PlaygroundProject:
    playground_input = PlaygroundInput(language=language, sourcecode=sourcecode, stdin=stdin)
    output = await run_playground(playground_input)
    return PlaygroundProject(title=title, **playground_input.model_dump(), **output.model_dump())


@router.get('', response_model=list[PlaygroundProject])
async def get_examples() -> list[PlaygroundProject]:
    key = 'codelab_examples'
    data = await redis.get(key)
    if data:
        logger.debug('Cached: Examples')
        return TypeAdapter(list[PlaygroundProject]).validate_json(data)

    logger.debug('Not Cached: Examples')
    # load examples
    tasks = []
    with (
        patch('app.codebox.TIMEOUT', None),
        patch('app.codebox.COMPILATION_TIMEOUT', None),
        patch('app.codebox.DATABASE_TIMEOUT', None),
    ):  # increase timeout for examples
        for example in (Path(__file__).parent.parent / 'examples').glob('*.toml'):
            project = tomli.loads(example.read_text())
            tasks.append(run_example(**project))
        examples = await asyncio.gather(*tasks)
    examples.sort(key=lambda x: (x.language, x.title))
    examples_dict = [x.model_dump() for x in examples]
    await redis.set(key, orjson.dumps(examples_dict), ex=config.TTL)
    return examples
