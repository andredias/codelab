# see: http://flask.pocoo.org/docs/0.10/config/

from flask.ext.babel import gettext as _

# SERVER_NAME = 'codelab.pronus.io'
APP_NAME = 'Code Lab'
DESCRIPTION = _('You can run, improve and share your sourcecode online with Code Lab!')

SECRET_KEY = b'\xf06\xe34\x93\xf0\xad\xa5\xe7\xde\xf1R' \
             b'\xb3\xef\xd9\xaa\x92J\x14\xea'

# TESTING = True

MAIL_SERVER = 'smtp.zoho.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'admin@pronus.io'
MAIL_DEFAULT_SENDER = 'codelab@pronus.io'

# Configurar em um outro arquivo não versionado as seguintes constantes:
# MAIL_PASSWORD = 'PasswordHere'

MAIL_RECEIVER = ['codelab@pronus.io']
