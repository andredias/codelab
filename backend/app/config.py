import os
from datetime import timedelta

ENV = os.environ['ENV'].lower()
if ENV not in ('development', 'testing', 'production'):
    raise ValueError(f'ENV="{ENV}" but it should be "development", "testing" or "production"')
TESTING = ENV == 'testing'
DEBUG = ENV != 'production'

LOG_LEVEL = os.getenv('LOG_LEVEL') or DEBUG and 'DEBUG' or 'INFO'

TTL = int(os.getenv('TTL', timedelta(days=3).total_seconds())) if not TESTING else 1
TIMEOUT = float(os.getenv('TIMEOUT', 0.1))
REDIS_URL = 'redis://localhost:6379' if DEBUG else 'redis://redis:6379'
CODEBOX_URL = 'http://localhost:8001' if DEBUG else 'http://codebox:8000'
