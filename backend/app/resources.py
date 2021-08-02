import sys
from string import ascii_uppercase

from aioredis import Redis
from loguru import logger
from tenacity import retry, stop_after_delay, wait_exponential

from . import config

redis = Redis.from_url(config.REDIS_URL)


async def startup() -> None:
    '''
    Initialize resources such as Redis and Database connections
    '''
    setup_logger()
    if config.DEBUG:
        show_config()
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


def show_config() -> None:
    values = {v: getattr(config, v) for v in sorted(dir(config)) if v[0] in ascii_uppercase}
    logger.debug(values)
    return


async def _init_redis():
    from .projects import load_examples

    # test redis connection
    @retry(stop=stop_after_delay(3), wait=wait_exponential(multiplier=0.2))
    async def _connect_to_redis() -> None:
        logger.debug('Connecting to Redis...')
        await redis.set('test_connection', '1234')
        await redis.delete('test_connection')

    await _connect_to_redis()
    await load_examples()
    return


async def _stop_redis():
    if config.TESTING:
        await redis.flushdb()
