from app.models import PlaygroundInput, Response, calc_hash


async def test_calc_hash() -> None:
    message = 'Hello World!'
    proj1 = PlaygroundInput(
        sourcecode=f'print("{message}")\n',
        language='python',
    )
    proj2 = PlaygroundInput(
        sourcecode=f'print("{message}!")\n',
        language='python',
    )

    id_proj1 = calc_hash(proj1)
    id_proj2 = calc_hash(proj2)

    assert len(id_proj1) == len(id_proj2) == 24
    assert id_proj1 != id_proj2
    assert id_proj1 == calc_hash(proj1)


def test_response() -> None:
    r1 = Response(stdout='Hello World!\n', stderr='', exit_code=0, elapsed_time=0.75)
    r2 = Response(stdout='Hello World!\n', stderr='', exit_code=0, elapsed_time=1)

    assert r1 == r2
    assert '750ms' in str(r1)
