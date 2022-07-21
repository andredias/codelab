from base64 import urlsafe_b64encode
from collections.abc import Callable
from hashlib import md5
from typing import Any, Optional

import orjson
from pydantic import BaseModel as _BaseModel

from .config import TIMEOUT

# ref: https://pydantic-docs.helpmanual.io/usage/exporting_models/#custom-json-deserialisation

default_type = Optional[Callable[[Any], Any]]


def orjson_dumps(v: _BaseModel, *, default: default_type) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class BaseModel(_BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


def calc_hash(obj: BaseModel) -> str:
    """
    Calculates the hash of any pydantic model.
    """
    return urlsafe_b64encode(md5(obj.json().encode()).digest()).decode()  # nosec: B324


# Codebox Related

Sourcefiles = dict[str, str]


class Command(BaseModel):
    command: str
    timeout: float = TIMEOUT
    stdin: str | None = None


class CodeboxInput(BaseModel):
    sources: Sourcefiles
    commands: list[Command]


class Response(BaseModel):
    stdout: str = ''
    stderr: str = ''
    exit_code: int = 0
    elapsed_time: float = 0

    def __str__(self) -> str:
        return (
            f'Response(stdout={self.stdout!r}, stderr={self.stderr!r}, '
            f'exit_code={self.exit_code!r}, elapsed_time={self.elapsed_time * 1000:.0f}ms)'
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Response)
            and self.stdout == other.stdout
            and self.stderr == other.stderr
            and self.exit_code == other.exit_code
            # elapsed_time is not compared because it is not guaranteed to be the same
        )


# Code Lab related


class PlaygroundInput(BaseModel):
    language: str
    sourcecode: str
    stdin: str | None


class PlaygroundOutput(BaseModel):
    id: str
    responses: list[Response]

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, PlaygroundOutput)
            and self.id == other.id
            and self.responses == other.responses
        )


class PlaygroundProject(PlaygroundInput, PlaygroundOutput):
    title: str = ''
