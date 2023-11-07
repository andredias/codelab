import asyncio
from pathlib import Path
from unittest.mock import patch

import orjson
import tomli
from fastapi import APIRouter
from loguru import logger
from pydantic import TypeAdapter

from .. import config
from ..codebox import run_codelab_project
from ..models import CodelabInput, CodelabProject
from ..resources import redis

router = APIRouter(prefix='/examples', tags=['examples'])


async def run_example(
    title: str, language: str, sourcecode: str, stdin: str = ''
) -> CodelabProject:
    codelab_input = CodelabInput(language=language, sourcecode=sourcecode, stdin=stdin)
    output = await run_codelab_project(codelab_input)
    return CodelabProject(title=title, **codelab_input.model_dump(), **output.model_dump())


@router.get('', response_model=list[CodelabProject])
async def get_examples() -> list[CodelabProject]:
    key = 'codelab_examples'
    data = await redis.get(key)
    if data:
        logger.debug('Cached: Examples')
        return TypeAdapter(list[CodelabProject]).validate_json(data)

    logger.debug('Not Cached: Examples')
    # load examples
    tasks = []
    with (
        patch('codelab.codebox.TIMEOUT', None),
        patch('codelab.codebox.COMPILATION_TIMEOUT', None),
        patch('codelab.codebox.DATABASE_TIMEOUT', None),
    ):  # disable timeout limit for examples
        for example in (Path(__file__).parent.parent / 'examples').glob('*.toml'):
            project = tomli.loads(example.read_text())
            tasks.append(run_example(**project))
        examples = await asyncio.gather(*tasks)
    examples.sort(key=lambda x: (x.language, x.title))
    examples_dict = [x.model_dump() for x in examples]
    await redis.set(key, orjson.dumps(examples_dict), ex=config.TTL)
    return examples
