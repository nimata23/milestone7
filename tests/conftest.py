import pytest
from website.__init__ import create_test_app, drop_database

@pytest.fixture()
def app():
    app = create_test_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

    drop_database(app)

@pytest.fixture()
def client(app):
    return app.client()