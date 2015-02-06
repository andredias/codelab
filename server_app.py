import logging
from app.server import app, manager
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('/tmp/codebox.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

if __name__ == '__main__':
    manager.run()
