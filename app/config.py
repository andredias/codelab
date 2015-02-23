# see: http://flask.pocoo.org/docs/0.10/config/

from flask.ext.babel import gettext as _

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


LANGUAGES = {  # name: mode
    'python': 'python',
    'c': 'c_cpp',
    'c++': 'c_cpp',
    'go': 'golang',
    'javascript': 'javascript',
    'ruby': 'ruby',
}

ACE_THEME = 'ace/theme/cobalt'


def get_redis_host():
    import sh
    redis_image = 'redis-server'
    host = sh.awk(sh.grep(sh.docker('inspect', redis_image), 'IPAddress'), '-F', '"', '{print $4}')
    return host

CACHE_REDIS_HOST = get_redis_host()
