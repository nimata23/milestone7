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
    assert user != None: "Error: User not created. Check models::User"
    assert user.email == "hannah25@colby.edu": "Error in models::User"
    assert user.first_name == "hannah": "Error in models::User"
    assert user.last_name =="soria": "Error in models::User"
    assert user.password == "1234567": "Error in models::User"
    assert user.role == "athlete": "Error in models::User"

def test_add_user_toDB(client):
    #create user and commit to db
    user = User(email = "hannah25@colby.edu", first_name = "hannah",
    last_name = "soria", password = "1234567", role = "athlete")
    db.session.add(user)
    db.commit()

    #try to get the user from databse
    test_find = User.query.filter_by(email="hannah25@colby.edu").first()
    #verify user information stored in db
    print("Email: " + test_find.email +" == hannah25@colby.edu")
    print("First name: "+ test_find.first_name + " == hannah")
    print("Last name: " + test_find.last_name + " == soria")
    print("Password: "+ test_find.password +" == 1234567")
    print("Role: " + test_find.role + " == athlete")
    
    #tests user is in DB and data was stored correctly
    assert user != None: "Error: User not created. Check models.User"
    assert test_find != None: "Error: user not found in database"
    assert test_find.role == "athlete": "Error: role stored db does not match role of user"
    #does not test email as email must match for user to be found
    assert test_find.first_name == "hannah": "Error: first name stored in db does not match first name of user"
    assert test_find.last_name == "soria":"Error: last name stored in db does not match first name of user"
    assert test_find.password == "1234567":"Error: password stored in db does not match first name of user"
    