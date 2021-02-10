from pathlib import Path
from typing import Any, Union

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .resources import shutdown, startup
from .routers import project

routers = [
    project.router,
]


def create_app(env_filename: Union[str, Path] = None) -> FastAPI:
    # a .env file is not mandatory. You can specify envvar parameters by other means
    if env_filename:
        load_dotenv(env_filename)

    app = FastAPI(default_response_class=ORJSONResponse)
    for router in routers:
        app.include_router(router)

    @app.on_event('startup')
    async def startup_event():
        await startup()

    @app.on_event('shutdown')
    async def shutdown_event():
        await shutdown()

    return app
