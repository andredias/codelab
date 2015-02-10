from app.server import app, manager


if __name__ == '__main__':
    app.config.update(
        DEBUG=True
    )
    manager.run()
