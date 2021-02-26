import os
from datetime import timedelta

DEBUG: bool
ENV: str
LOG_LEVEL: str
REDIS_URL: str
TESTING: bool
TIMEOUT: float
TTL: int


def init():

    global DEBUG
    global ENV
    global LOG_LEVEL
    global REDIS_URL
    global TESTING
    global TIMEOUT
    global TTL

    ENV = os.environ['ENV'].lower()
    if ENV not in ('development', 'testing', 'production'):
        raise ValueError(f'ENV="{ENV}" but it should be "development", "testing" or "production"')
    TESTING = ENV == 'testing'
    DEBUG = ENV != 'production'

    LOG_LEVEL = os.getenv('LOG_LEVEL') or DEBUG and 'DEBUG' or 'INFO'

    TTL = int(os.getenv('TTL', timedelta(days=3).total_seconds())) if not TESTING else 1
    TIMEOUT = float(os.getenv('TIMEOUT', 0.1))
    REDIS_URL = os.getenv('REDIS_URL') or 'redis://localhost:6379'
