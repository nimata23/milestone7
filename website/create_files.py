from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from datetime import date, datetime

today = date.today()
t = today.strftime("%m/%d/%Y")
lt = datetime.now()
curr_time = lt.strftime("%H:%M:%S")
date_time = t + "_" + curr_time + "_"

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/upload/drive/v3/files']

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
media = MediaFileUpload('./data/{0}'.format('sleep.csv'), mimetype='text/csv')
media1 = MediaFileUpload('./data/{0}'.format('readiness.csv'), mimetype='text/csv')
media2 = MediaFileUpload('./data/{0}'.format('nutrition.csv'), mimetype='text/csv')

service.files().create(body=file_metadata, media_body = media, fields= 'id').execute()
service.files().create(body=file_metadata1, media_body = media1, fields= 'id').execute()
service.files().create(body=file_metadata2, media_body = media2, fields= 'id').execute()


#add create
