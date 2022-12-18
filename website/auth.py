from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Hawkins, Team
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = User.query.filter_by(email=email).first()
        except:
            user = None
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                if user.role == 'athlete':
                    first_name = user.first_name
                    last_name = user.last_name
                    return redirect(url_for('views.athleteView',first_name=first_name, last_name=last_name))
                elif user.role == 'coach':
                    team_name = user.teams[0].name
                    return redirect(url_for('views.teamView',team_name=team_name))
                elif user.role == 'admin':
                    return redirect(url_for('views.adminView'))
                else:
                    flash('User role not recognized, please contact admin')
            else:
                flash('Incorrect password')
        else:
            flash('Email does not exist')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/permissions', methods=['GET', 'POST'])
def permissions():
    try:
        user_list = User.query.all() 
        team_list = Team.query.all()
    except:
        user_list = []
        team_list = []

    id = request.form.get('users')
    if id:
        selected_user = User.query.filter_by(id=request.form.get('users')).first()
    else:
        selected_user = current_user
    
    selected_role = request.form.get('select_role')
    if not selected_role:
        selected_role = 'athlete'


    if request.method == 'POST':
        add_user = request.form.get('new_user')
        delete_user = request.form.get('delete_user')

        if add_user == 'true':
            email = request.form.get('email')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            role = request.form.get('roles')
            teams = request.form.get('teams')
            emailList = email.split('@')

            user = User.query.filter_by(email=email).first()

            fields_valid = validate_fields(first_name, last_name, user)
            email_valid = validate_email(email, emailList)
            password_valid = validate_password(password, confirm_password)
            if role == 'athlete' or 'coach':
                teams_valid = validate_team(teams)
            else:
                teams_valid == True
        
            if fields_valid and email_valid and password_valid and teams_valid:
                create_user(email, password, role, first_name, last_name, teams)
        
        if delete_user == 'true':
            user_id = request.form.get('delete_options')
            deleted_user = User.query.filter_by(id=user_id).first()
            if(deleted_user):
                db.session.delete(deleted_user)
                db.session.commit()
                flash('User has been deleted')
            else:
                flash('This user does not exist. Try refreshing the page to see the updated user list.')

    

    return render_template("permissions.html", user=current_user, user_list=user_list, chosen_user=selected_user,
            selected_role=selected_role, team_list = team_list)

def validate_email(email, emailList):
    isValid = True
    if email == '':
        flash('Notice: Email required.')
        isValid = False
    elif len(emailList) < 2:
        flash('Notice: Invalid email.')
        isValid = False
    elif emailList[1] != 'colby.edu':
        flash('Notice: Must use colby email.')
        isValid = False
    elif len(email) < 4:
        flash('Notice: Email must be greater than 3 characters.')
        isValid = False
    return isValid
    
def validate_password(password, confirm_password):
    isValid = True
    regexp = re.compile('[^0-9a-zA-Z]+')
    if len(password) < 7:
        flash('Notice: Password must be at least 7 characters.')
        isValid=False
    elif password != confirm_password:
        flash('Notice: Passwords do not match.')
        isValid = False
    elif password.islower():
        flash('Notice: Password must include at least 1 capital letter.')
        isValid = False
    elif not re.search('[0-9]', password) and not regexp.search(password):
        flash('Notice: Password must contain at least 1 number or special character.')
        isValid = False
    elif not re.search('[a-zA-Z]', password):
        isValid = False
        flash('Notice: Password must contain at least 1 alphabetic character [a-z] or [A-Z].')
    return isValid 

def validate_fields(first_name, last_name, user):
    isValid = True
    if user:
        flash('Notice: There is already a user associated with this email.')
        isValid = False
    elif  first_name == '':
        flash('Notice: First name field cannot be empty.')
        isValid = False
    elif last_name == '':
        flash('Notice: Last name field cannot be empty.')
        isValid = False
    return isValid

def validate_team(teams):
    isValid = True
    if not teams:
        flash('Notice: Athletes and Coaches must be assigned to a team.')
        isValid = False
        return isValid

    for team in teams:
        t = Team.query.filter_by(id=team)
        if not t:
            isValid = False
            flash('Notice: There is no team by that name in the database.')
    return isValid

def create_user(email, password, role, first_name, last_name, teams):
    print("Happened")
            
    # add user to database
    new_user = User(email=email,
                    password=generate_password_hash(password, method='sha256'),
                    role=role, first_name=first_name, last_name=last_name)
    if role == 'athlete':
        for team in teams:
            t = Team.query.filter_by(id=team).first()
            t.users += [new_user]
    db.session.add(new_user)
    db.session.commit()
            
    flash('Account created!', category='success')
    return


