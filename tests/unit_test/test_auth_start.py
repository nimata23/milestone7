import pytest
from website.auth import User

def new_user():
    user = User(email = "hannah@colby.edu", first_name = "hannah",
    last_name = "soria", password = "1234567", role = "athlete")
    return user

def test_role():
    user = new_user()
    role = user.role 
    assert role == "athlete"
    assert role != "coach"
    assert role != "admin"

def test_email():
    user = new_user()
    email = user.email
    assert email == "hannah@colby.edu"
    assert email != "hanah@colby.edu"