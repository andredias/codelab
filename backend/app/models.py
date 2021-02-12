from typing import Optional

from pydantic import BaseModel

Sourcefiles = dict[str, str]


class Command(BaseModel):
    type: Optional[str]
    command: str
    timeout: Optional[float] = None
    input: Optional[str] = None


class CodeboxInput(BaseModel):
    sources: Sourcefiles
    commands: list[Command]


class Response(BaseModel):
    stdout: str = ''
    stderr: str = ''
    exit_code: int


Responses = list[Response]


class Description(BaseModel):
    title: str = ''
    description: str = ''


class Project(Description, CodeboxInput):
    id: str
    responses: Responses = []


class ProjectResponses(BaseModel):
    id: str
    responses: Responses = []
