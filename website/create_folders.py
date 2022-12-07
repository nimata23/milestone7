#from .Google import Create_Service
from Google import Create_Service
CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

data = ['Sleep_Backup', 'Readiness_Backup', 'Nutrition_Backup']

for info in data:
    file_metadata = {
        'name': info,
        'mimeType': 'application/vnd.google-apps.folder'
        #'parents': ["API_testing"]
    }

    service.files().create(body=file_metadata).execute()