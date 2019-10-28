import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('authorization_data_for_google_api.json', scope)
contacts = []


def auth():
    global sheet
    global client
    client = gspread.authorize(creds)
    sheet = client.open('Silaedr').worksheet('контакты учеников')
    sheet = sheet.get_all_values()

    
def clear():
    global contacts
    contacts = []


def check(a, b):
    d = []
    for i in range(len(a)):
        d.append([0] * (len(b)))
    if a[0] != b[0]:
        d[0][0] = 1
    for k in range(1, len(b)):
        if a[0] == b[k]:
            d[0][k] = k
        else:
            d[0][k] = d[0][k - 1] + 1
    for g in range(1, len(a)):
        if b[0] == a[g]:
            d[g][0] = g
        else:
            d[g][0] = d[g - 1][0] + 1
    for i in range(1, len(a)):
        for j in range(1, len(b)):
            if a[i] == b[j]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j - 1], d[i - 1][j], d[i][j - 1]) + 1
    # for i in range(len(d)):
    #    print(d[i])
    f = d[-1][-1]
    return f


def send_to_class(klass):
    f = False
    global contacts
    for i in range(len(sheet)):
        if sheet[i][0] == klass:
            if len(sheet[i][sheet[0].index('e-mail матери')]) > 8:
                contacts.append(sheet[i][sheet[0].index('e-mail матери')])
            if len(sheet[i][sheet[0].index('e-mail отца')]) > 8:
                contacts.append(sheet[i][sheet[0].index('e-mail отца')])
            f = True
        elif f:
            break


def send_to_children(grade):
    global contacts
    f = False
    for i in range(len(sheet)):
        if sheet[i][0] == grade:
            if len(sheet[i][sheet[0].index('e-mail ребенка')]) > 8:
                contacts.append(sheet[i][sheet[0].index('e-mail ребенка')])
            f = True
        elif f:
            break


def send_to_all():
    global contacts
    auth()
    for i in range(1, len(sheet)):
        if len(sheet[i][sheet[0].index('e-mail матери')]) > 8:
            contacts.append(sheet[i][sheet[0].index('e-mail матери')])
        if len(sheet[i][sheet[0].index('e-mail отца')]) > 8:
            contacts.append(sheet[i][sheet[0].index('e-mail отца')])
        if len(sheet[i][sheet[0].index('e-mail ребенка')]) > 8:
            contacts.append(sheet[i][sheet[0].index('e-mail ребенка')])
    send_to_teachers()


def send_to_some(crit):
    auth()
    global contacts
    crit = [i for i in crit.split()]
    name = []
    print(crit)
    for i in range(len(crit)):
        if crit[i][0].isupper():
            name.append(crit[i])
    print(name)
    j = sheet[0].index('e-mail матери')
    for i in range(1, len(sheet)):
        if name[1][:len(name[1])-2] in sheet[i][sheet[0].index('Фамилия')]:
            contacts.append(sheet[i][j])
            break


def auth_teachers():
    global sheet1
    sheet1 = client.open('Silaedr').worksheet('контакты учителей')
    sheet1 = sheet1.get_all_values()
    print(sheet1)

def send_to_teachers():
    global  contacts
    auth_teachers()
    for e in sheet1:
        contacts.append(e[5])
