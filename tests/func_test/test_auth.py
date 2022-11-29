import pytest
from website.models import User
from website import db
#from werkzeug.security import generate_password_hash

def test_create_user():
    #create user
    user = User(email = "hannah25@colby.edu", first_name = "hannah",
    last_name = "soria", password = "1234567", role = "athlete")

    #verify user information
    print("Email: " + user.email +" == hannah25@colby.edu")
    print("First name: "+ user.first_name + " == hannah")
    print("Last name: " + user.last_name + " == soria")
    print("Password: "+ user.password +" == 1234567")
    print("Role: " + user.role + " == athlete")

    #test if user object can be created, test data is stored correctly
    assert user != None
    assert user.email == "hannah25@colby.edu"
    assert user.first_name == "hannah"
    assert user.last_name =="soria"
    assert user.password == "1234567"
    assert user.role == "athlete"


    