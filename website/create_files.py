from .Google import Create_Service
from googleapiclient.http import MediaFileUpload
from datetime import date, datetime
import os.path

from flask import Flask, Blueprint, render_template

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# from flask import Flask, Blueprint, redirect, url_for
# from flask_login import login_required

# create_files = Blueprint('create_files', __name__)

# @create_files.route('/backup')
# @login_required
def make_files():
    today = date.today()
    t = today.strftime("%m/%d/%Y")
    lt = datetime.now()
    curr_time = lt.strftime("%H:%M:%S")
    date_time = t + "_" + curr_time + "_"

    CLIENT_SECRET_FILE = 'credentials_driveapi.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/drive']

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
                'credentials_driveapi.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        folder_id = [["1UKhfm-HGVrbFd08IHOmNZEPdT9o9RNsb"], ["1WefTYqEm76xD1q-YCaPiomXvBg4PQRnb"], ["1zM7aSKyTwu4j_jWejhAmIfqBCso1x74s"]]

        #fix mimetype for csv
        file_metadata = {'name': date_time + 'sleep.csv', 'parents': folder_id[0]}
        #service.files().create(body=file_metadata).execute()
        file_metadata1 = {'name': date_time + 'readiness.csv', 'parents': folder_id[1]}
        #service.files().create(body=file_metadata1).execute()
        file_metadata2 = {'name': date_time + 'nutrition.csv', 'parents': folder_id[2]}
        #service.files().create(body=file_metadata2).execute()

        #add media - point files to data folder
        media = MediaFileUpload('./website/data/{0}'.format('sleep.csv'), mimetype='text/csv')
        media1 = MediaFileUpload('./website/data/{0}'.format('readiness.csv'), mimetype='text/csv')
        media2 = MediaFileUpload('./website/data/{0}'.format('nutrition.csv'), mimetype='text/csv')

        service.files().create(body=file_metadata, media_body = media, fields= 'id').execute()
        service.files().create(body=file_metadata1, media_body = media1, fields= 'id').execute()
        service.files().create(body=file_metadata2, media_body = media2, fields= 'id').execute()
        #add create
        # return render_template('views.adminView')
    
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')



make_files()