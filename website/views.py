from urllib import request

from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, current_app, redirect
from flask_login import login_required, current_user, login_user

from . import db
from .models import User, Hawkins, parse_csv
from werkzeug.utils import secure_filename
import os

import pandas as pd

import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from werkzeug.security import generate_password_hash

import sys


views = Blueprint('views', __name__)


@views.route("/", methods=['GET','POST'])
def home():
    return redirect(url_for('auth.login'))


@views.route("/adminView",methods=['GET','POST'])
@login_required
def adminView():
    tmR = pd.read_csv('csvs/TeamNames.csv')
    TeamNames = tmR["TeamNames"].tolist()

    dfR = pd.read_csv('website/data/readiness.csv')
    readinessAvg = dfR["Score"].mean().astype(int)

    dfS = pd.read_csv('website/data/sleep.csv')
    hoursAvg = dfS["Hours"].mean().astype(int)

    qualityAvg = dfS["Quality"].mean().astype(int)

    dfN = pd.read_csv('website/data/nutrition.csv')
    calAvg = dfN["Calorie Intake"].mean().astype(int)

    dfT = pd.read_csv('website/data/team.csv')
    teamValues1 = dfT["Hours"].tolist()
    teamValues2 = dfT["Readiness"].tolist()

    readinessL = ["Score"]
    readinessV = [readinessAvg]

    sleepL = ["Hours", "Quality"]
    h = [hoursAvg]
    q = [qualityAvg]

    nutritionL = ["Calorie Intake"]
    nutritionV = [calAvg]

    fig = make_subplots(rows=1, cols=4, column_widths=[.2, .2, .2, .5],
                        subplot_titles=["Readiness", "Sleep", "Nutrition",
                                        "Team Readiness"],
                        horizontal_spacing=0.1,
                        specs=[[{"type": "pie"}, {"type": "pie"},
                                {"type": "pie"}, {"type": "scatter"}]])

    # READINESS GRAPH
    fig.add_trace(go.Pie(values=readinessV, labels=readinessL, hole=.5,
                         title="Readiness", textfont=dict(color="white")),
                  row=1, col=1)

    # SLEEP GRAPH
    fig.add_trace(go.Pie(title="Sleep", hole=0.5, sort=False,
                         direction='clockwise', values=q,
                         textposition='inside',
                         marker={'line': {'color': 'white', 'width': 1}}),
                  row=1, col=2)

    fig.add_trace(go.Pie(hole=0.7, sort=False, direction='clockwise', values=h,
                         labels=sleepL, textposition='inside',
                         marker={'colors': ['green', 'red', 'blue'],
                                 'line': {'color': 'white', 'width': 1}}),
                  row=1, col=2)

    # NUTRITION GRAPH
    fig.add_trace(go.Pie(values=nutritionV, labels=nutritionL, hole=.5,
                         title="Nutrition", textfont=dict(color="white")),
                  row=1, col=3)

    # TEAM GRAPH
    fig.add_trace(go.Scatter(x=teamValues1, y=teamValues2), row=1, col=4)

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                      'paper_bgcolor': 'rgba(0,0,0,0)', })

    fig.update_layout(margin=dict(l=50, r=0, t=0, b=0))
    fig.update_layout(showlegend=False)
    fig.update_layout(width=1100, height=300)
    fig.update_layout(font_color="white")
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template("adminView.html", user=current_user,
    graphJSON=graphJSON, team_names=TeamNames )

@views.route("/teamView/<team_name>", methods=['GET','POST'])
@login_required
def teamView(team_name):

    anR = pd.read_csv('csvs/user.csv')
    First = anR["first_name"].tolist()
    Last = anR["last_name"].tolist()
    names = []
    for i in range(len(First)):
        names += [(First[i], Last[i])]
    

    dfR = pd.read_csv('website/data/readiness.csv')
    readinessAvg = dfR["Score"].mean().astype(int)

    dfS = pd.read_csv('website/data/sleep.csv')
    hoursAvg = dfS["Hours"].mean().astype(int)

    qualityAvg = dfS["Quality"].mean().astype(int)

    dfN = pd.read_csv('website/data/nutrition.csv')
    calAvg = dfN["Calorie Intake"].mean().astype(int)

    dfT = pd.read_csv('website/data/team.csv')
    teamValues1 = dfT["Hours"].tolist()
    teamValues2 = dfT["Readiness"].tolist()

    readinessL = ["Score"]
    readinessV = [readinessAvg]

    sleepL = ["Hours", "Quality"]
    h = [hoursAvg]
    q = [qualityAvg]

    nutritionL = ["Calorie Intake"]
    nutritionV = [calAvg]

    fig = make_subplots(rows=1, cols=4, column_widths=[.2, .2, .2, .5],
                        subplot_titles=["Readiness", "Sleep", "Nutrition",
                                        "Team Readiness"],
                        horizontal_spacing=0.1,
                        specs=[[{"type": "pie"}, {"type": "pie"},
                                {"type": "pie"}, {"type": "scatter"}]])

    # READINESS GRAPH
    fig.add_trace(go.Pie(values=readinessV, labels=readinessL, hole=.5,
                         title="Readiness", textfont=dict(color="white")),
                  row=1, col=1)

    # SLEEP GRAPH
    fig.add_trace(go.Pie(title="Sleep", hole=0.5, sort=False,
                         direction='clockwise', values=q,
                         textposition='inside',
                         marker={'line': {'color': 'white', 'width': 1}}),
                  row=1, col=2)

    fig.add_trace(go.Pie(hole=0.7, sort=False, direction='clockwise', values=h,
                         labels=sleepL, textposition='inside',
                         marker={'colors': ['green', 'red', 'blue'],
                                 'line': {'color': 'white', 'width': 1}}),
                  row=1, col=2)

    # NUTRITION GRAPH
    fig.add_trace(go.Pie(values=nutritionV, labels=nutritionL, hole=.5,
                         title="Nutrition", textfont=dict(color="white")),
                  row=1, col=3)

    # TEAM GRAPH
    fig.add_trace(go.Scatter(x=teamValues1, y=teamValues2), row=1, col=4)

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                      'paper_bgcolor': 'rgba(0,0,0,0)', })

    fig.update_layout(margin=dict(l=50, r=0, t=0, b=0))
    fig.update_layout(showlegend=False)
    fig.update_layout(width=1100, height=300)
    fig.update_layout(font_color="white")
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("teamView.html",user=current_user,
                       graphJSON=graphJSON, athletes=names, TeamName =team_name)


@views.route("/athleteView/<first_name><last_name>", methods=['GET','POST'])
def athleteView(first_name, last_name):
   # name = athlete_name[0] + athlete_name[1]
    if request.method == "POST": 
        return flask.redirect(authorization_url)


    dfR = pd.read_csv('website/data/readiness.csv')
    readinessAvg = dfR["Score"].mean().astype(int)

    dfS = pd.read_csv('website/data/sleep.csv')
    hoursAvg = dfS["Hours"].mean().astype(int)

    qualityAvg = dfS["Quality"].mean().astype(int)

    dfN = pd.read_csv('website/data/nutrition.csv')
    calAvg = dfN["Calorie Intake"].mean().astype(int)

    dfT = pd.read_csv('website/data/team.csv')
    teamValues1 = dfT["Hours"].tolist()
    teamValues2 = dfT["Readiness"].tolist()

    readinessL = ["Score"]
    readinessV = [readinessAvg]

    sleepL = ["Hours", "Quality"]
    h = [hoursAvg]
    q = [qualityAvg]

    nutritionL = ["Calorie Intake"]
    nutritionV = [calAvg]

    fig = make_subplots(rows=1, cols=4, column_widths=[.2, .2, .2, .5],
                        subplot_titles=["Readiness", "Sleep", "Nutrition",
                                        "Team Readiness"],
                        horizontal_spacing=0.1,
                        specs=[[{"type": "pie"}, {"type": "pie"},
                                {"type": "pie"}, {"type": "scatter"}]])

    # READINESS GRAPH
    fig.add_trace(go.Pie(values=readinessV, labels=readinessL, hole=.5,
                         title="Readiness", textfont=dict(color="white")),
                  row=1, col=1)

    # SLEEP GRAPH
    fig.add_trace(go.Pie(title="Sleep", hole=0.5, sort=False,
                         direction='clockwise', values=q,
                         textposition='inside',
                         marker={'line': {'color': 'white', 'width': 1}}),
                  row=1, col=2)

    fig.add_trace(go.Pie(hole=0.7, sort=False, direction='clockwise', values=h,
                         labels=sleepL, textposition='inside',
                         marker={'colors': ['green', 'red', 'blue'],
                                 'line': {'color': 'white', 'width': 1}}),
                  row=1, col=2)

    # NUTRITION GRAPH
    fig.add_trace(go.Pie(values=nutritionV, labels=nutritionL, hole=.5,
                         title="Nutrition", textfont=dict(color="white")),
                  row=1, col=3)

    # TEAM GRAPH
    fig.add_trace(go.Scatter(x=teamValues1, y=teamValues2), row=1, col=4)

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                      'paper_bgcolor': 'rgba(0,0,0,0)', })

    fig.update_layout(margin=dict(l=50, r=0, t=0, b=0))
    fig.update_layout(showlegend=False)
    fig.update_layout(width=1100, height=300)
    fig.update_layout(font_color="white")
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("athleteView.html",user=current_user,
                            graphJSON=graphJSON, fname=first_name, lname=last_name)
 
 

@views.route("/permissions", methods=['GET', 'POST'])
def permissions():

    try:
        list = User.query.all()
        
        user_list = list
        print(len(user_list))
    except:
        user_list = []
    id = request.form.get('users')
    if id:
        selected_user = User.query.filter_by(id=id).first()
    else:
        selected_user = current_user
    
    selected_role = "Athlete"

    if request.method == "POST":
        selected_role = request.form.get("select_role")
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name= request.form.get('last_name')
        password = request.form.get('password')
        role = request.form.get('roles')
        
        try:
            emailList = email.split('@')
        except:
            emailList = ["no","no"]
            
        
        try:
            user = User.query.filter_by(email=email).first()
        except:
            user = False
        if user:
            flash('Email already exists.', category='error')
        elif emailList[1] != 'colby.edu':
            flash('Must use colby email', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            
            # add user to database
            new_user = User(email=email,
                            password=generate_password_hash(password, method='sha256'),
                            role=role, first_name=first_name, last_name=last_name)

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
    
        
    return render_template("permissions.html", user=current_user, user_list=user_list, selected_role=selected_role,selected_user=selected_user)


@views.route("/athleteDetail",methods=['GET','POST'])
def athleteDetail():
    return render_template("athleteDetail.html")

# helper function for upload()
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {"csv"}

@views.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            # parse the csv file and insert it into the db
            data_type = filename.rsplit(".")[0].lower()
            parse_csv(data_type=data_type, filename=filename)
            return redirect(url_for("views.upload"))

    # basic, flask-provided html for uploading files
    # TODO make an actual webpage that imlements this
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



