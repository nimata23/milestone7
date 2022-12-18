import pytest

#tests creating a new user, the new user should not be created as the passwords do not match.
def test_failed_password_match(client):
    response = client.get('/permissions',follow_redirects=True)
    #assert login page is stable
    assert response.status_code == 200
    # assert email and password boxes are available to users for login
    assert b'Admin Permissions Page' in response.data

    with client:
        # try to login with with wrong password 
        response = client.post("/permissions", data={"first_name": "gru", "last_name":"Al Madi",
        "email": "gru@colby.edu", "password": "GruIsC00l", "confirm_password": "GruIscool", "roles":'admin'})
        #assert page is still stable
        print(response.data)
        assert response.status_code == 200
        #assert correct error message is displayed
        assert b'Notice: Passwords do not match.' in response.data

        
#tests creating a new user, the new user should not be created as there is no password given.
def test_failed_no_password(client):
    response = client.get('/permissions')
    #assert login page is stable
    assert response.status_code == 200
    # assert email and password boxes are available to users for login
    assert b'Admin Permissions Page' in response.data

    with client:
        # try to login with with wrong password 
        response = client.post("/permissions", data={"first_name": "gru", "last_name": "Al Madi",
        "email": "gru@colby.edu", "password": "", "confirm_password": "", "roles":'admin'})
        #assert page is still stable
        response = client.get('/permissions', follow_redirects=True)
        assert response.status_code == 200
        #assert correct error message is displayed
        assert b'Notice: Password and password confirmation are required' in response.data


#tests creating a new user, the new user should not be created as the password was not confirmed.
def test_failed_no__conf_password(client):
    response = client.get('/permissions')
    #assert login page is stable
    assert response.status_code == 200
    # assert email and password boxes are available to users for login
    assert b'Admin Permissions Page' in response.data

    with client:
        # try to login with with wrong password 
        response = client.post("/permissions", data={"first_name": "gru", "last_name": "Al Madi",
        "email": "gru@colby.edu", "password": "gruIsC00l", "confirm_password": "", "roles":'admin'})
        #assert page is still stable
        assert response.status_code == 200
        #assert correct error message is displayed
        assert b'Notice: Password and password confirmation are required' in response.data