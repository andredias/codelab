import os
from datetime import timedelta

DEBUG: bool
ENV: str
LOG_LEVEL: str
REDIS_URL: str
TESTING: bool
TIMEOUT: int


def init():

    global DEBUG
    global ENV
    global LOG_LEVEL
    global REDIS_URL
    global TESTING
    global TIMEOUT

    ENV = os.environ['ENV'].lower()
    if ENV not in ('development', 'testing', 'production'):
        raise ValueError(f'ENV="{ENV}" but it should be "development", "testing" or "production"')
    TESTING = ENV == 'testing'
    DEBUG = ENV != 'production'

    LOG_LEVEL = os.getenv('LOG_LEVEL') or DEBUG and 'DEBUG' or 'INFO'

    default_timeout = timedelta(days=30).total_seconds()
    TIMEOUT = int(os.getenv('TIMEOUT') or default_timeout)
    REDIS_URL = os.environ['REDIS_URL'] or 'redis://localhost:6379'
