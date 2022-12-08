from __future__ import print_function

import json
import os.path
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.


# The ID and range of a sample spreadsheet.

quickstart = Blueprint('quickstart', __name__)


#SAMPLE_SHEETS_ID ="1BuQdt1HK9g17WOdJOSkN1n0HGtUTv9HcmOB7QDqg9Jg"
CREDENTIALS = "website/credentials.json"
SAMPLE_RANGE_NAME = 'Sheet1!A1:K50'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

@quickstart.route('/<string:dataId>', methods=['POST'])
@login_required
def read_sheets(dataId):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    sheets_id = json.loads(dataId)

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId= sheets_id,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        else:
            print(values)
        
    except HttpError as err:
        print(err)
    first_name = current_user.first_name
    last_name = current_user.last_name
    return redirect('views.athleteView',first_name = first_name,
        last_name = last_name)

