import asyncio
import sys
from time import sleep, time
from typing import Any, Awaitable, Callable, Union

from aioredis import create_redis_pool
from aioredis.commands import Redis
from loguru import logger

from . import config

redis: Redis = None


async def startup() -> None:
    '''
    Initialize resources such as Redis and Database connections
    '''
    config.init()
    setup_logger()
    await _init_redis()
    logger.info('started...')


async def shutdown() -> None:
    '''
    Release resources
    '''
    await _stop_redis()
    logger.info('...shut down')


def setup_logger():
    '''
    Configure Loguru's logger
    '''

    _intercept_standard_logging_messages()
    logger.remove()  # remove standard handler
    logger.add(
        sys.stderr, level=config.LOG_LEVEL, colorize=True, backtrace=config.DEBUG, enqueue=True
    )  # reinsert it to make it run in a different thread
    logger.debug({key: getattr(config, key) for key in dir(config) if key == key.upper()})


def _intercept_standard_logging_messages():
    '''
    Intercept standard logging messages toward loguru's logger
    ref: loguru README
    '''
    import logging

    class InterceptHandler(logging.Handler):

        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=0)


async def _init_redis():
    global redis
    function = create_redis_pool(config.REDIS_URL)
    redis = await wait_until_responsive(function)
    return


async def _stop_redis():
    if config.TESTING:
        await redis.flushdb()
    redis.close()
    await redis.wait_closed()


async def wait_until_responsive(
    function: Union[Awaitable, Callable], timeout: float = 3.0, interval: float = 0.1
) -> Any:
    ref = time()
    while (time() - ref) < timeout:
        try:
            if asyncio.iscoroutine(function):
                result = await function  # type:ignore
            else:
                result = function()  # type:ignore
            return result
        except:  # noqa: E722
            pass
        sleep(interval)
    raise TimeoutError()
