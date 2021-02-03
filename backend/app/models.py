from typing import List, Optional, Mapping

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


class Output(BaseModel):
    stdout: Optional[str]
    stderr: Optional[str]
    lints: Optional[Mapping[str, List[Lint]]]
    metrics: Optional[Mapping[str, List[Metric]]]


class ProjectOut(BaseModel):
    id: str
    output: Output


class ProjectCore(BaseModel):
    sources: List[Sourcefile]
    build_command: str = ''
    run_command: str
    input: str = ''


class ProjectIn(ProjectCore):
    title: str = ''
    description: str = ''


class Project(ProjectIn, ProjectOut):
    pass
