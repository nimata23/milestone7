import pytest
from website.models import User
#from website import db, create_test_app
from werkzeug.security import check_password_hash

def test_success_login_coach(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'email' in response.data
    assert b'password' in response.data

    with client:
        response = client.post("/login", data={"email": "hannah@colby.edu",
            "password": "1234567890"})
        assert response.status_code == 302
        assert b'Redirecting' in response.data

        response = client.get('/teamView/<team_name>', follow_redirects=True)
        assert response.status_code == 200
        assert b"Home" in response.data
    


    