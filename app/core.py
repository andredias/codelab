import sh
import json
import logging
from hashlib import md5

CONTAINER = 'codelab'

logger = logging.getLogger('core')
logger.setLevel(logging.INFO)
sl = logging.StreamHandler()
sl.setLevel(logging.INFO)
logger.addHandler(sl)


def run(project):
    params = json.dumps(project)
    logger.info(params)
    output = sh.docker.run('-i', '--rm', '--net', 'none', CONTAINER, _ok_code=range(3),
                           _in=params)
    logger.info(output)
    return json.loads(str(output)) if output else {}


def project_id(source, language, input='', **kwargs):
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
