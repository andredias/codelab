import os
from datetime import timedelta

CODEBOX_URL: str
DEBUG: bool
ENV: str
LOG_LEVEL: str
REDIS_URL: str
TESTING: bool
TIMEOUT: float
TTL: int


def init():

    global CODEBOX_URL
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
    REDIS_URL = 'redis://localhost:6379' if TESTING else 'redis://redis:6379'
    CODEBOX_URL = 'http://localhost:8001' if TESTING else 'http://codebox:8000'
