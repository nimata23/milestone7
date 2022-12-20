# imports
from urllib import request
from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, current_app, redirect
from flask_login import login_required, current_user, login_user
from . import db
from .models import User, Team
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

# create blueprint
views = Blueprint('views', __name__)

# goes to login
@views.route("/", methods=['GET','POST'])
def home():
    return redirect(url_for('auth.login'))

# admin view
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

# path to specific team
@views.route("/teamView/<team_name>", methods=['GET','POST'])
@login_required
def teamView(team_name):

    anR = pd.read_csv('csvs/user.csv')
    First = anR["first_name"].tolist()
    Last = anR["last_name"].tolist()
    names = []
    for i in range(len(First)):
        names += [(First[i], Last[i])]
    
    # read in csv files for the team view
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

   # read in csv for the athlete view
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
 
 













