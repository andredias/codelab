import pytest

from app.codebox import run_playground_in_codebox
from app.models import PlaygroundInput


@pytest.mark.parametrize(
    ('language', 'sourcecode', 'stdin'),
    [
        ('rust', 'fn main() { println!("Hello World!"); }', None),
        ('bash', 'echo "Hello World!"', None),
        ('sqlite3', 'SELECT 1;', None),
        pytest.param('non-existent-language', 'tra-la-la', '123', marks=pytest.mark.xfail),
    ],
)
async def test_run_playground_in_codebox(language: str, sourcecode: str, stdin: str | None) -> None:
    playground_input = PlaygroundInput(
        sourcecode=sourcecode,
        language=language,
        stdin=stdin,
    )
    responses = await run_playground_in_codebox(playground_input)
    assert len(responses) >= 1
