from datetime import datetime, timezone
from typing import Any, Callable, Optional

import orjson
from pydantic import BaseModel as _BaseModel
from pydantic import validator

# ref: https://pydantic-docs.helpmanual.io/usage/exporting_models/#custom-json-deserialisation


default_type = Optional[Callable[[Any], Any]]


def orjson_dumps(v: _BaseModel, *, default: default_type) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class BaseModel(_BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


# Codebox Related

Sourcefiles = dict[str, str]


class Command(BaseModel):
    command: str
    timeout: float | None = None
    stdin: str | None = None


class CodeboxProject(BaseModel):
    sources: Sourcefiles
    commands: list[Command]


class Response(BaseModel):
    stdout: str = ''
    stderr: str = ''
    exit_code: int = 0
    elapsed_time: float = 0


# Code Lab related


class ProjectDescription(BaseModel):
    title: str = ''
    description: str = ''


class ProjectToRun(ProjectDescription):
    language: str
    sourcecode: str
    stdin: str | None


class ProjectResponse(Response):
    id: str


class CodelabProject(ProjectToRun, ProjectResponse):

    timestamp: datetime | None = None

    @validator('timestamp', pre=True, always=True)
    def set_ts_now(cls, v: datetime) -> datetime:  # noqa: N805
        """
        See: https://pydantic-docs.helpmanual.io/usage/validators/#validate-always

        This validation might become unnecessary in Pydantic 2.0
        and be replaced by something like 'timestamp: datetime = datetime.now
        see: https://github.com/samuelcolvin/pydantic/pull/12108
        """
        return v or datetime.now(timezone.utc)
