from app.models import Command, ProjectDescriptionCore, Response
from app.projects import calc_id, run_project_in_container


async def test_calc_id():
    message = 'Hello World!'
    timeout = 0.1
    proj1 = ProjectDescriptionCore(
        sources={'main.py': f'print("{message}")\n'},
        commands=[Command(command='python main.py', timeout=timeout)],
    )
    proj2 = ProjectDescriptionCore(
        sources={'source.py': f'print("{message}")\n'},
        commands=[Command(command='python source.py', timeout=timeout)],
    )

    id_proj1 = calc_id(proj1)
    id_proj2 = calc_id(proj2)

    assert len(id_proj1) == len(id_proj2) == 32
    assert id_proj1 != id_proj2
    assert id_proj1 == calc_id(proj1)


async def test_run_project_in_container():
    project_core = ProjectDescriptionCore(
        sources={'main.py': 'print("Olá mundo!")\n'},
        commands=[Command(command='python main.py', timeout=0.1)],
    )
    responses = await run_project_in_container(project_core)
    assert responses == [Response(stdout='Olá mundo!\n', stderr='', exit_code=0)]


async def test_load_examples(examples):
    assert examples
