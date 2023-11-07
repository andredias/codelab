from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from . import config  # noqa: F401
from .exception_handlers import request_validation_exception_handler
from .middleware import log_request_middleware
from .resources import lifespan
from .routers import examples, playground

app = FastAPI(
    title='Codelab',
    lifespan=lifespan,
)

routers = (
    examples.router,
    playground.router,
)
for router in routers:
    app.include_router(router)

origins = (
    'http://localhost:8080',
    'http://localhost:3000',
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
