from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from .resources import shutdown, startup
from .routers import examples, playground

routers = [
    examples.router,
    playground.router,
]

origins = [
    'http://localhost:8080',
    'http://localhost:3000',
]

app = FastAPI(
    title='Codelab',
    default_response_class=ORJSONResponse,
    on_startup=(startup,),
    on_shutdown=(shutdown,),
)

for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
