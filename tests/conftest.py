import pytest
from website import create_app, drop_database

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

    drop_database(app)

@pytest.fixture()
def client(app):
    return app.client()