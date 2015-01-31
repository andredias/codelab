# see: http://flask.pocoo.org/docs/0.10/config/

# SERVER_NAME = 'codelab.pronus.io'
APP_NAME = 'Code Lab'
DESCRIPTION = 'You can run, improve and share your sourcecode online with Code Lab!'

SECRET_KEY = b'\xf06\xe34\x93\xf0\xad\xa5\xe7\xde\xf1R' \
             b'\xb3\xef\xd9\xaa\x92J\x14\xea'

# TESTING = True

MAIL_SERVER = 'data9.nspmanaged.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'pronus@pronus.eng.br'

# Configurar em um outro arquivo não versionado as seguintes constantes:
# MAIL_PASSWORD = 'PasswordHere'

ADMINS = ['andref.dias@pronus.eng.br', 'codelab@pronus.io']
