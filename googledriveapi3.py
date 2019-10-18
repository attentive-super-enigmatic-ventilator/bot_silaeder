import os
from __future__ import print_function
import pickle

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from downloading_google_sheet.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

creds = None
if os.path.exists('client-secrets.dat'):
    with open('client-secrets.dat', 'rb') as f:
        creds = pickle.load(f)
if creds is None or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('client-secrets.dat', 'wb') as f:
        pickle.dump(creds, f)

gauth = GoogleAuth()
gauth.credentials = GoogleCredentials(access_token=creds.token, \
                                      client_id=creds.client_id, \
                                      refresh_token=creds.refresh_token, \
                                      token_expiry=creds.expiry, \
                                      token_uri=creds.token_uri, \
                                      client_secret=creds.client_secret, \
                                      user_agent='MoSanya FireVov')

drive = GoogleDrive(gauth)
folder_id = open("folder.dat").read().strip()
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    lister = drive.ListFile({'q': "'%s' in parents" % folder_id}).GetList()

print(len(lister))
for item in lister:

    mimetypes = {
        'application/vnd.downloading_google_sheet-apps.document': 'application/pdf',

        'application/vnd.downloading_google_sheet-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    }
    download_mimetype = None
    for item in lister:
        item.GetContentFile('base_of_photos/' + item['title'])