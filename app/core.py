import sh
import json
import logging

CONTAINER = 'codebox'

logger = logging.getLogger('core')
logger.setLevel(logging.INFO)
sl = logging.StreamHandler()
sl.setLevel(logging.INFO)
logger.addHandler(sl)


def run(project):
    params = json.dumps(project)
    logger.info(params)
    output = sh.docker.run('-i', '--rm', CONTAINER, _ok_code=range(3),
                           _in=params)
    logger.info(output)
    return json.loads(str(output)) if output else {}
