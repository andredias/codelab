import json
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE

from app.models import CodeboxInput, Command, Response  # isort:skip

TIMEOUT = 0.1

core = CodeboxInput(
    sources={
        'main.py':
            'print("Olá mundo!")\n',
        'app/array.py':
            '''a = [1, 2, 3, 4, 5]
print(a[::2])  # iterate over the whole list in 2-increments
print(a[::-1])  # a useful idiom for 'x reversed'
'''
    },
    commands=[
        Command(command=f'sleep {TIMEOUT + 0.1}', timeout=TIMEOUT),
        Command(command='python main.py'),
        Command(command='python app/array.py', input='Olá\nAçúcar'),
        Command(command='cat hello.py'),
        Command(command='cat main.py'),
    ]
)

responses = [
    Response(stdout='', stderr=f'Timeout Error. Exceeded {TIMEOUT}s', exit_code=-1),
    Response(stdout='Olá mundo!\n', stderr='', exit_code=0),
    Response(stdout='[1, 3, 5]\n[5, 4, 3, 2, 1]\n', stderr='', exit_code=0),
    Response(stdout='', stderr='cat: hello.py: No such file or directory\n', exit_code=1),
    Response(stdout='print("Olá mundo!")\n', stderr='', exit_code=0)
]


async def test_container():
    project_json = core.json(ensure_ascii=False).encode()
    docker_cmd = ['docker', 'run', '-i', '--rm', 'codebox']
    proc = await create_subprocess_exec(*docker_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate(input=project_json)
    assert stderr == b''
    assert responses == [Response(**resp) for resp in json.loads(stdout)]
