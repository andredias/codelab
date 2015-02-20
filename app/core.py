import sh
import json
from hashlib import md5

CONTAINER = 'codelab'


def run(project):
    params = json.dumps(project)
    output = sh.docker.run('-i', '--rm', '--net', 'none', CONTAINER, _ok_code=range(3),
                           _in=params)
    return json.loads(output.stdout.decode('utf-8'))


def project_id(source, language, input=''):
    s = '{input}{source}{language}'.format(input=input, source=source, language=language)
    return md5(s.encode('utf-8')).hexdigest()


def cache_project(cache, project):
    if 'id' not in project:
        project['id'] = project_id(**project)
    output = run(project)
    if output:
        project.update(output)
        cache.set(project['id'], project)
    return
