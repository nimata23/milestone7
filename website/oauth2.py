
import pandas as pd
import os
CLIENT_SECRET_FILE = 'website/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'

def read_files():
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=google_sheet_id,
            dody= request_body_json
        )
        return response
    except Exception as e:
        print(e)
        return None

def main():
    service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

if __name__ == "__main__":
    main()

