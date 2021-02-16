from typing import Optional

import orjson
from pydantic import BaseModel as _BaseModel

# ref: https://pydantic-docs.helpmanual.io/usage/exporting_models/#custom-json-deserialisation


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class BaseModel(_BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


Sourcefiles = dict[str, str]


class Command(BaseModel):
    type: Optional[str] = None
    command: str
    timeout: Optional[float] = None
    input: Optional[str] = None


class ProjectCore(BaseModel):
    sources: Sourcefiles
    commands: list[Command]


class Response(BaseModel):
    stdout: str = ''
    stderr: str = ''
    exit_code: int = 0


class ProjectDescriptionCore(ProjectCore):
    title: str = ''
    description: str = ''


class Project(ProjectDescriptionCore):
    id: str
    responses: list[Response] = []


class ProjectResponses(BaseModel):
    id: str
    responses: list[Response] = []
