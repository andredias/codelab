import logging
from server.server import app, manager
from logging.handlers import RotatingFileHandler

if __name__ == '__main__':
    handler = RotatingFileHandler('/tmp/codebox.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    manager.run()
