# see: http://flask.pocoo.org/docs/0.10/config/

from collections import OrderedDict
from flask_babel import gettext as _

# SERVER_NAME = 'codelab.pronus.io'
APP_NAME = 'Code Lab'
DESCRIPTION = _('Code Lab is an online editor, runner and linter for Python, Ruby, C/C++ and '
                'other programming languages')
SOCIAL_MEDIA = _('Code Lab: Nothing like being able to run my code online...')

SECRET_KEY = b'\xf06\xe34\x93\xf0\xad\xa5\xe7\xde\xf1R' \
             b'\xb3\xef\xd9\xaa\x92J\x14\xea'

MAIL_SERVER = 'smtp.zoho.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'admin@pronus.io'
MAIL_DEFAULT_SENDER = 'codelab@pronus.io'

# Configurar em um outro arquivo não versionado as seguintes constantes:
# MAIL_PASSWORD = 'PasswordHere'

MAIL_RECEIVERS = ['codelab@pronus.io']


LANGUAGES = OrderedDict([
    ('python', {'ace-mode': 'python', 'logo': 'images/python.svg', 'label': 'Python (3)',
                'pygments': 'python'}),
    ('c', {'ace-mode': 'c_cpp', 'logo': 'images/c.svg', 'label': 'C', 'pygments': 'c'}),
    ('c++', {'ace-mode': 'c_cpp', 'logo': 'images/cpp.svg', 'label': 'C++',
             'pygments': 'c++'}),
    ('go', {'ace-mode': 'golang', 'logo': 'images/go.png', 'label': 'Go',
            'pygments': 'go'}),
    ('javascript', {'ace-mode': 'javascript', 'logo': 'images/javascript.png',
                    'label': 'Javascript (Node.js)', 'pygments': 'javascript'}),
    ('ruby', {'ace-mode': 'ruby', 'logo': 'images/ruby.svg', 'label': 'Ruby',
              'pygments': 'ruby'}),
    ('sql', {'ace-mode': 'sql', 'logo': 'images/sqlite.svg', 'label': 'SQL (SQLite)',
             'pygments': 'sql'}),
    ('bash', {'ace-mode': 'sh', 'logo': 'images/terminal.svg', 'label': 'Bash',
              'pygments': 'bash'}),
])

ACE_THEME = 'ace/theme/cobalt'


def get_redis_host():
    import socket
    try:
        socket.gethostbyname('redis')
        return 'redis'
    except socket.gaierror:
        return 'localhost'

CACHE_REDIS_HOST = get_redis_host()
