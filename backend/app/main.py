from pathlib import Path
from typing import Any, Union

import orjson
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.responses import JSONResponse

from .resources import shutdown, startup
# from .routers import

routers = [

]


class ORJSONResponse(JSONResponse):

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


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
