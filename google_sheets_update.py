import pickle
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('authorization_data_for_google_api.json', scope)
contacts = []
google_sheet_name = open("google_sheet_name.dat").read().splitlines()[0]

while True:
    try:
        client = gspread.authorize(creds)
        sheet2 = client.open(google_sheet_name).worksheet('Расписание 2019').get_all_values()
        pickle.dump(sheet2, open("google_sheets_data.dat", "wb"))
        time.sleep(60)
    except Exception as er:
        print(er)
        pass




