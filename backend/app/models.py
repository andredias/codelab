from base64 import urlsafe_b64encode
from hashlib import md5

from pydantic import BaseModel

from .config import TIMEOUT

# ref: https://pydantic-docs.helpmanual.io/usage/exporting_models/#custom-json-deserialisation


def calc_hash(obj: BaseModel) -> str:
    """
    Calculates the hash of any pydantic model.
    """
    return (
        urlsafe_b64encode(md5(obj.model_dump_json().encode()).digest())  # noqa: S324
        .decode()
        .rstrip('=')
    )


# Codebox Related

Sourcefiles = dict[str, str]


class Command(BaseModel):
    command: str
    timeout: float | None = TIMEOUT
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
    stdin: str | None = None


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
