from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from .resources import shutdown, startup
from .routers import playground

routers = [
    playground.router,
]

origins = [
    'http://localhost:8080',
    'http://localhost:3000',
]


def create_app() -> FastAPI:

    app = FastAPI(default_response_class=ORJSONResponse)
    for router in routers:
        app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    @app.on_event('startup')
    async def startup_event() -> None:
        await startup()

    @app.on_event('shutdown')
    async def shutdown_event() -> None:
        await shutdown()

    return app
