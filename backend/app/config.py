import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('ENV', 'production').lower()
if ENV not in ('production', 'development', 'testing'):
    raise ValueError(
        f'ENV={ENV} is not valid. ' "It should be 'production', 'development' or 'testing'"
    )
DEBUG = ENV != 'production'
TESTING = ENV == 'testing'

LOG_LEVEL = os.getenv('LOG_LEVEL') or (DEBUG and 'DEBUG') or 'INFO'
os.environ['LOGURU_DEBUG_COLOR'] = '<fg #777>'

TTL = int(os.getenv('TTL', timedelta(days=3).total_seconds())) if not TESTING else 1
TIMEOUT = float(os.getenv('TIMEOUT', 0.1))
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
CODEBOX_URL = os.getenv('CODEBOX_URL', 'http://localhost:8000')
