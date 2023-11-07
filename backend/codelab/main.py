from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .resources import lifespan
from .routers import examples, playground

app = FastAPI(
    title='Codelab',
    debug=config.DEBUG,
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
