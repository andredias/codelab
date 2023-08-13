from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from redis.asyncio import Redis
from tenacity import RetryError, retry, stop_after_delay, wait_exponential

from . import config

redis = Redis.from_url(config.REDIS_URL)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:  # noqa: ARG001
    await startup()
    try:
        yield
    finally:
        await shutdown()


async def startup() -> None:
    show_config()
    await connect_redis()
    logger.info('started...')


async def shutdown() -> None:
    await disconnect_redis()
    logger.info('...shutdown')


def show_config() -> None:
    config_vars = {key: getattr(config, key) for key in sorted(dir(config)) if key.isupper()}
    logger.debug(config_vars)


async def connect_redis() -> None:

    # test redis connection
    @retry(stop=stop_after_delay(3), wait=wait_exponential(multiplier=0.2))
    async def _connect_to_redis() -> None:
        logger.debug('Connecting to Redis...')
        await redis.ping()

    try:
        await _connect_to_redis()
    except RetryError:
        logger.error('Could not connect to Redis')
        raise


async def disconnect_redis() -> None:
    if config.TESTING:
        await redis.flushdb()
    await redis.close()
