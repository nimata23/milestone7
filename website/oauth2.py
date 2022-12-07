from __future__ import print_function
from datetime import datetime, timedelta
import os.path
import requests
from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, current_app, redirect, session, jsonify
from flask_login import login_required, current_user, login_user

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

oauth2 = Blueprint('oauth2', __name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/fitness.heart_rate.read',
        'https://www.googleapis.com/auth/fitness.nutrition.read',
        'https://www.googleapis.com/auth/fitness.sleep.read']

CREDS = 'website/credentials.json'

@oauth2.route('/test_cred')
def api_request():
    if 'credentials' not in session:
        return redirect(url_for('oauth2.authorize'))

    credentials = Credentials(**session['credentials'])

    try:
        fitness_service = build('fitness', 'v1', credentials=credentials)
        source_url = 'https://www.googleapis.com/fitness/v1/users/me/dataSources'
        data_url = 'https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate'
        headers={'content-type':'application/json', 'Authorization':'Bearer%s'%credentials}

        data_sources = requests.get(source_url, headers)
        print(data_sources.status_code)
        # Call the Drive v3 API
        now = datetime.now()
        one_week_ago = now - timedelta(days=7)
        #str_now = now.strptime("%d.%m.%Y %H:%M:%S")
        #str_week = one_week_ago.strptime("%d.%m.%Y %H:%M:%S")
        end = now.timestamp()*1000
        start = one_week_ago.timestamp()*1000

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

    session['credentials'] = credentials_to_dict(credentials)
    #return jsonify(**files)

@oauth2.route('/oauth2')
def authorize():
    #create flow instance 
    flow = InstalledAppFlow.from_client_secrets_file(CREDS, SCOPES)
    flow.redirect_uri = url_for('oauth2.oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type ='offline',
        include_granted_scopes = 'true')

    session['state'] = state
    return redirect(authorization_url)

@oauth2.route('/oauth2callback')
def oauth2callback():
    state = session['state']

    flow = InstalledAppFlow.from_client_secrets_file(
        CREDS, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2.oauth2callback', _external=True)

    authorization_respose = request.url
    flow.fetch_token(authorization_response=authorization_respose)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('oauth2.api_request'))

def credentials_to_dict(credentials):
    return {'token':credentials.token,
            'refresh_token':credentials.refresh_token,
            'token_uri':credentials.token_uri,
            'client_id':credentials.client_id,
            'client_secret':credentials.client_secret,
            'scopes': credentials.scopes}

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_slient_secrets_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            flow.redirect_uri = 'https://localhost/oauth2callback'
            #authorization_url, state=flow.authorization_url(access_type = 'offline',
            #    included_granted_scopes='true')
            #return redirect(authorization_url)

        session['credentials'] = credentials_to_dict()
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    try:
        fitness_service = build('fitness', 'v1', credentials=creds)
        source_url = 'https://www.googleapis.com/fitness/v1/users/me/dataSources'
        data_url = 'https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate'
        headers={'content-type':'application/json', 'Authorization':'Bearer%s'%creds}

        data_sources = requests.get(source_url, headers)
        print(data_sources.status_code)
        # Call the Drive v3 API
        now = datetime.now()
        one_week_ago = now - timedelta(days=7)
        #str_now = now.strptime("%d.%m.%Y %H:%M:%S")
        #str_week = one_week_ago.strptime("%d.%m.%Y %H:%M:%S")
        end = now.timestamp()*1000
        start = one_week_ago.timestamp()*1000

    
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')
    


if __name__ == '__main__':
    main()