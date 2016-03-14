import json
import logging
from subprocess import check_output

CONTAINER = 'codebox'

logger = logging.getLogger('core')
logger.setLevel(logging.INFO)
sl = logging.StreamHandler()
sl.setLevel(logging.INFO)
logger.addHandler(sl)


def run(project):
    params = json.dumps(project)
    logger.info(params)
    output = check_output(['docker', 'run', '-i', '--rm', CONTAINER], input=params, universal_newlines=True)
    logger.info(output)
    return json.loads(str(output)) if output else {}
