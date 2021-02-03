from typing import Optional

from pydantic import BaseModel


class Lint(BaseModel):
    line: int
    column: Optional[int]
    code: str
    message: str
    level: str
    linter: str


class Metric(BaseModel):
    name: str
    value: float


class Sourcefile(BaseModel):
    path: str
    code: str


class Command(BaseModel):
    command: str
    timeout: Optional[float]


class Output(BaseModel):
    stdout: Optional[str]
    stderr: Optional[str]
    lints: Optional[list[str, list[Lint]]]
    metrics: Optional[dict[str, list[Metric]]]


class ProjectOut(BaseModel):
    id: str
    output: Output


class ProjectCore(BaseModel):
    sources: list[Sourcefile]
    commands: list[Command]
    input: str = ''


class ProjectIn(ProjectCore):
    title: str = ''
    description: str = ''


class Project(ProjectIn, ProjectOut):
    pass
