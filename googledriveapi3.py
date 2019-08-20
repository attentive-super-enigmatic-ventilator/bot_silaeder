from __future__ import print_function
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import google.auth.transport
from oauth2client.client import GoogleCredentials

gauth = GoogleAuth()
if os.path.isfile("mycreds.txt") is False:
    choice = input ("Do you want to: U) Upload authentication file (mycreds.txt). B) Browser authentication (only possible for owner of the connected Google drive folder). [U/B]? : ")
    if choice == "U":
          print("Upload the mycreds.txt file")
          from google.colab import files
          files.upload()
    elif choice == "B":
          google.auth.authenticate_user()
          gauth.credentials = GoogleCredentials.get_application_default()
          gauth.SaveCredentialsFile("mycreds.txt")

gauth.LoadCredentialsFile("mycreds.txt")
if gauth.access_token_expired:
    gauth.Refresh()
else: gauth.Authorize()

drive = GoogleDrive(gauth)
folder_id = open("folder.txt").read()
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
print(file_list)
for file1 in file_list:
  print('title: %s, id: %s' % (file1['title'], file1['id']))
lister = drive.ListFile({'q': "'%s' in parents" % folder_id}).GetList()

print(len(lister))
for item in lister:
    print(item['title'])
    print('title: %s, mimeType: %s' % (item['title'], item['mimeType']))
    mimetypes = {
        'application/vnd.google-apps.document': 'application/pdf',

        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    }
    download_mimetype = None
    for item in lister:
        print(item['title'])
        print(item['id'])
        print(item)
        item.GetContentFile('/home/alexandr/PycharmProjects/chatbot/base_of_photos/' + item['title'])