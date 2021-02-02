from httpx import AsyncClient
from loguru import logger


async def test_run_project(client: AsyncClient) -> None:
    logger.info('project')
    pass
