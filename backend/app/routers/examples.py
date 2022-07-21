from pathlib import Path

import orjson
import tomli
from fastapi import APIRouter
from loguru import logger
from pydantic import parse_obj_as

from .. import config
from ..codebox import run_playground
from ..models import PlaygroundInput, PlaygroundProject
from ..resources import redis

router = APIRouter(prefix='/examples', tags=['examples'])


@router.get('', response_model=list[PlaygroundProject])
async def get_examples() -> list[PlaygroundProject]:
    key = 'codelab_examples'
    data = await redis.get(key)
    if data:
        logger.debug('Cached: Examples')
        return parse_obj_as(list[PlaygroundProject], orjson.loads(data))

    logger.debug('Not Cached: Examples')
    # load examples
    examples = []
    for example in (Path(__file__).parent.parent / 'examples').glob('*.toml'):
        project = tomli.loads(example.read_text())
        playground_input = PlaygroundInput(**project)
        output = await run_playground(playground_input)
        if any(r.exit_code != 0 for r in output.responses):
            logger.error(f'Example failed: {project["title"]}, {output}')
        playground_project = PlaygroundProject(**project, **output.dict())
        examples.append(playground_project)
    examples.sort(key=lambda x: (x.language, x.title))
    examples_dict = [x.dict() for x in examples]
    await redis.set(key, orjson.dumps(examples_dict), ex=config.TTL)
    return examples
