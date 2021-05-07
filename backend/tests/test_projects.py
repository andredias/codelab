from app.models import ProjectToRun, Response
from app.projects import calc_id, run_project_in_codebox


async def test_calc_id():
    message = 'Hello World!'
    proj1 = ProjectToRun(
        sourcecode=f'print("{message}")\n',
        language='python',
    )
    proj2 = ProjectToRun(
        title='Hello World',
        sourcecode=f'print("{message}")\n',
        language='python',
    )

    id_proj1 = calc_id(proj1)
    id_proj2 = calc_id(proj2)

    assert len(id_proj1) == len(id_proj2) == 32
    assert id_proj1 != id_proj2
    assert id_proj1 == calc_id(proj1)


async def test_run_project_in_codebox(docker):
    project_core = ProjectToRun(
        sourcecode='print("Olá mundo!")\n',
        language='python',
    )
    responses = await run_project_in_codebox(project_core)
    assert responses == Response(stdout='Olá mundo!\n', stderr='', exit_code=0)
