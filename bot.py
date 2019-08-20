import os
import glob
import random
import urllib.request
from sys import stderr

import vk
import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import mimetypes
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
import face_recognition

import google
import photos_encoding

user_service_access_key = open("user_service_access_key.txt").read().splitlines()[0]
service_access_key = open('service.txt').read().splitlines()
session = vk.Session(access_token=service_access_key)
api1 = vk.API(session, v=5.101)
owner_id = open('owner.txt').read().splitlines()
admins = {str(i) for i in open('admins.txt').read().splitlines()}
loginpassword = open('login_password.txt').read().splitlines()
mail1 = open('mail.txt').read().splitlines()
tokens = open('secret.txt').read().splitlines()
vk_session = vk_api.VkApi(token=tokens[0])
vko = vk_session.get_api()
app_id = open('app.txt').read().splitlines()
sessio = vk.Session(access_token=user_service_access_key)
api = vk.API(sessio, v=5.101)
contacts = []
"""vk_sessio = vk_api.VkApi(loginpassword[0], loginpassword[1], app_id=int(app_id  [0]), scope='wall, photos')
vk_sessio.auth()
upload = vk_api.VkUpload(vk_sessio)"""

test_image_encodings = []
quantity_faces = []


def sendmail(text1, files):
    mail = smtplib.SMTP('smtp.mail.ru', 587)
    msg = MIMEMultipart()
    msg['From'] = mail1[0]
    msg['Subject'] = 'Новости Силаэдра'
    msg.attach(MIMEText(text1, 'plain'))
    for filepath in files:
        filename = os.path.basename(filepath)

        if os.path.isfile(filepath):
            ctype, encoding = mimetypes.guess_type(filepath)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                with open(filepath) as fp:
                    file = MIMEText(fp.read(), _subtype=subtype)
                    fp.close()
            elif maintype == 'image':
                with open(filepath, 'rb') as fp:
                    file = MIMEImage(fp.read(), _subtype=subtype)
                    fp.close()
            elif maintype == 'audio':
                with open(filepath, 'rb') as fp:
                    file = MIMEAudio(fp.read(), _subtype=subtype)
                    fp.close()
            else:
                with open(filepath, 'rb') as fp:
                    file = MIMEBase(maintype, subtype)
                    file.set_payload(fp.read())
                    fp.close()
                encoders.encode_base64(file)
            file.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(file)
    # mail.send_message(msg, to_addrs=contacts)
    mail.quit()


# sendmail('тест', ['C:/Users/user/Desktop/bot_silaedr/secret.txt', 'C:/Users/user/Desktop/bot_silaedr/1.jpg'])
flag = False
base = VkKeyboard(one_time=True)
base.add_button('Отправить', color=VkKeyboardColor.POSITIVE)
base.add_button('help', color=VkKeyboardColor.POSITIVE)
base = base.get_keyboard()


def create_keyb1(buttons):
    keyboard = VkKeyboard(one_time=True)
    for b in buttons:
        if b == 'new_line':
            keyboard.add_line()
        else:
            keyboard.add_button(b, color=VkKeyboardColor.POSITIVE)
    keyboard = keyboard.get_keyboard()
    return keyboard


def create_keyb(buttons):
    keyboard = VkKeyboard(one_time=True)
    for b in buttons:
        if b == 'new_line':
            keyboard.add_line()
        else:
            keyboard.add_button(b, color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Отменить отправку', color=VkKeyboardColor.NEGATIVE)
    keyboard = keyboard.get_keyboard()
    return keyboard


folder = 'photos'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

stop = VkKeyboard(one_time=True)
stop.add_button('Отменить отправку', color=VkKeyboardColor.NEGATIVE)
stop = stop.get_keyboard()

f_mail = False
f_group = False
news = ''
users = {}
# while True:
#    try:
print("Successfully started", file=stderr)
one_more_flag = False
for event in vk_api.longpoll.VkLongPoll(vk_session).listen():
    if event.type == vk_api.longpoll.VkEventType.MESSAGE_NEW and event.to_me and str(event.user_id) in admins:
        if event.user_id not in users:
            users[event.user_id] = 0
        incorrect_command = True
        inf = (vko.users.get(user_ids=event.user_id)[0])
        text = event.text.lower()
        if text == 'отменить отправку':
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Отправка отменена! Обращайтесь, когда появятся новости!',
                              keyboard=create_keyb1(['Отправить', 'help']))
            news = ''
            incorrect_command = False
            f_group = False
            f_mail = False
            users[event.user_id] = 0
            contacts = []
            folder = 'photos'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            continue
        if text == 'нет, спасибо':
            f_group = False
            f_mail = False
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Хорошо! Обращайтесь, когда появятся еще новости!',
                              keyboard=base)
            users[event.user_id] = 0
            if len(contacts) != 0:
                sendmail(news, glob.glob("photos/*.jpg"))
            contacts = []
            news = ''
            incorrect_command = False
            folder = 'photos'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
        if text == 'отправить ранее выбранным контактам' or text == 'отправить новость':
            if not f_group:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Новость отправлена на почту выбранным контактам!' +
                                          ' Вы хотите отправить новость еще куда-нибудь?',
                                  keyboard=create_keyb1(['Группа ВК', 'new_line', 'Нет, спасибо']))
                f_mail = True
                users[event.user_id] = 2
                if len(contacts) != 0:
                    sendmail(news, glob.glob("photos/*.jpg"))
            else:
                f_group = False
                f_mail = False
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Новость отправлена на почту выбранным контактам! ' +
                                          'Обращайтесь, когда появятся еще новости!',
                                  keyboard=base)
                users[event.user_id] = 0
                if len(contacts) != 0:
                    sendmail(news, glob.glob("photos/*.jpg"))
                contacts = []
                news = ''
                incorrect_command = False
                folder = 'photos'
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)
            incorrect_command = False
        if users[event.user_id] == 1 and text == 'нет':
            users[event.user_id] = 2
            one_more_flag = True
            incorrect_command = False
        if users[event.user_id] == 1 and text == 'да':
            google.auth()
            google.send_to_some(str(name[0] + ' ' + name[1]))
            contacts = google.contacts
            google.clear()
            sendmail(news, glob.glob("photos/*.jpg"))
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Новость отправлена! Обращайтесь, когда появятся еще новости!',
                              keyboard=base)
            users[event.user_id] = 0
            contacts = []
            news = ''
            incorrect_command = False
            folder = 'photos'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            continue
        if users[event.user_id] == 1:
            result = []
            news = event.text
            flag = False
            photos = api1.messages.getById(message_ids=event.message_id, group_id=183112747)
            for i in range(len(photos['items'][0]['attachments'])):
                length = len(photos['items'][0]['attachments'][i]['photo']['sizes']) - 1
                urllib.request.urlretrieve(photos['items'][0]['attachments'][i]['photo']['sizes'][length]['url'],
                                           'photos/' + str(i) + '.jpg')
            face = False
            test_image_encodings = []
            quantity_faces = []
            for i in glob.glob("photos/*.jpg"):
                test_image = face_recognition.load_image_file(i)
                test_image_locations = face_recognition.face_locations(test_image)
                if not test_image_locations == []:
                    test_image_encoding = face_recognition.face_encodings(test_image, test_image_locations)[0]
                    test_image_encodings.append(test_image_encoding)
                    quantity_faces.append(test_image_locations)
            if not quantity_faces == []:
                for i in photos_encoding.known_faces_encodings.keys():
                    for j in test_image_encodings:
                        comparing = face_recognition.compare_faces([photos_encoding.known_faces_encodings[i]], j)[0]
                        if comparing:
                            result.append(i)
                            name = i.split('/')[-1].split('_')
                            name[1] = name[1][:len(name[1])-4]
                            vko.messages.send(user_id=event.user_id,
                                              random_id=random.randint(1, 10 ** 9),
                                              message='Вы хотите отправить сообщение на почту родителям ребенка, ' +
                                              'который есть на этой фотографии? (' +
                                              i.split('/')[-1].split('_')[0] + ' ' +
                                              i.split('/')[-1].split('_')[1][:len(i.split('/')[-1].split('_')[1])-4]
                                              + ')', keyboard=create_keyb1(['Да', 'Нет']))
                            face = True
                if face:
                    continue
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Куда Вы хотите отправить новость?',
                              keyboard=create_keyb(['Группа ВК',  'Почта']))
            incorrect_command = False
            users[event.user_id] = 2
            continue
        if text == 'отправить':
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Напишите мне, что Вы хотите разослать. ' +
                                      'При необходимости Вы можете прикрепить файлы к сообщению.',
                              keyboard=stop)
            flag = True
            users[event.user_id] = 1
            incorrect_command = False
        if 'привет' in text:
            if vko.users.get(user_ids=event.user_id, fields=['sex'])[0]['sex'] == 2:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Привет, ' + (inf['first_name']) + ' ' +
                                  inf['last_name'] + '!' + ' Я рад, что ты мне написал!',
                                  keyboard=base)
            else:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Привет, ' + (inf['first_name']) + ' ' +
                                          inf['last_name'] + '!' + ' Я рад, что ты мне написала!',
                                  keyboard=base)
            incorrect_command = False
        if users[event.user_id] == 10:
            if 'родителям' in text:
                google.send_to_class(grade)
                contacts += google.contacts
                google.clear()
            elif 'ученикам' in text:
                google.send_to_children(grade)
                contacts += google.contacts
                google.clear()
            elif 'всем' in text:
                google.send_to_class(grade)
                google.send_to_children(grade)
                contacts += google.contacts
                google.clear()
            users[event.user_id] = 3
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Вы хотите отправить новость еще кому-нибудь? Если хотите, то напишите кому еще' +
                                      ' надо отправить новость, а если хотите отправить новость ранее выбранным' +
                                      ' контактам, то нажмите на кнопку "Отправить ранее выбранным контактам".' +
                                      '\n' + 'Для отмены отправки нажмите на кнопку "Отменить отправку"',
                              keyboard=create_keyb(
                                  ['5 С', '6 С', '7 С', 'new_line', '7 Т', '8 Л', '9 С', 'new_line', 'Учителям',
                                   'Отправить ранее выбранным контактам']))
            continue
        if users[event.user_id] == 3:
            cont = False
            to_all = False
            incorrect_command = False
            grade = '0'
            google.auth()
            for i in range(len(text)):
                try:
                    grade = str(int(text[i])) + ' '
                    grade += text[i+2].upper()
                    break
                except:
                    pass
            if grade != '0':
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Кому Вы хотите отправить новость?',
                                  keyboard=create_keyb(['Родителям(' + grade + ')', 'Ученикам(' + grade + ')',
                                                        'Всем(' + grade + ')']))
                cont = True
                users[event.user_id] = 10
            elif 'абсолютно всем' in text:
                google.send_to_all()
                contacts += google.contacts
                google.clear()
                to_all = True
            elif 'учителям' in text:
                google.send_to_teachers()
                contacts += google.contacts
                google.clear()
            else:
                google.send_to_some(event.text)
                contacts += google.contacts
                google.clear()
            if to_all:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Подтвердите отправку', keyboard=create_keyb(['Отправить новость']))
            elif not cont:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Вы хотите отправить новость еще кому-нибудь? Если хотите, то ' +
                                  'напишите кому еще надо отправить новость, а если хотите отправить новость ранее ' +
                                  'выбранным контактам, то нажмите на кнопку "Отправить ранее выбранным контактам".' +
                                  '\n' + 'Для отмены отправки нажмите на кнопку "Отменить отправку"',
                                  keyboard=create_keyb(['5 С', '6 С', '7 С', 'new_line', '7 Т', '8 Л', '9 С',
                                                        'new_line', 'Учителям', 'Отправить ранее выбранным контактам']))
        if text == 'почта' and users[event.user_id] == 2 or one_more_flag:
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Кому Вы хотите отправить новость? Вы можете отправить новость всем родителям ' +
                                      'определенного класса с помощью кнопок снизу.' + '\n' +
                                      'Также Вы можете отправить новость конкретным родителям, написав сообщение типа' +
                                      '"маме <Имя ребенка> <Фамилия ребенка>" или ' +
                                      '"отцу <Имя ребенка> <Фамилия ребенка>".',
                              keyboard=create_keyb(['5 С', '6 С', '7 С', 'new_line', '7 Т', '8 Л', '9 С', 'new_line',
                                                    'Учителям', 'Абсолютно всем']))
            users[event.user_id] = 3
            incorrect_command = False
            one_more_flag = False
        if text == 'опубликовать новость' and users[event.user_id] == 2:
            photos = glob.glob("photos/*.jpg")
            if len(photos) != 0:
                photo_list = upload.photo_wall(photos)
                attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
                api.wall.post(owner_id=owner_id, message=news, attachments=attachment)
            else:
                api.wall.post(owner_id=owner_id, message=news)
            f_group = True
            if not f_mail:
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Новость выложена в группе Силаэдра в ВК! Вы хотите отправить ее еще ' +
                                          'куда-нибудь?',
                                  keyboard=create_keyb1(['Почта', 'new_line', 'Нет, спасибо']))
            else:
                f_group = False
                f_mail = False
                vko.messages.send(user_id=event.user_id,
                                  random_id=random.randint(1, 10 ** 9),
                                  message='Новость выложена в группе Силаэдра в ВК! Обращайтесь, когда появятся еще' +
                                          ' новости!',
                                  keyboard=base)
                users[event.user_id] = 0
                if len(contacts) != 0:
                    sendmail(news, glob.glob("photos/*.jpg"))
                contacts = []
                news = ''
                incorrect_command = False
                folder = 'photos'
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)
            incorrect_command = False
        if text == 'группа вк' and users[event.user_id] == 2:
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Подтвердите публикацию новости',
                              keyboard=create_keyb(['Опубликовать новость']))
            incorrect_command = False
        if text == 'сайт' and users[event.user_id] == 2:
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='К сожалению, сайт Силаэдра пока не работает! Вы хотите отправить новость ' +
                                      'еще куда-нибудь?',
                              keyboard=create_keyb1(['Группа ВК', 'Сайт', 'Почта', 'new_line', 'Нет, спасибо']))
            incorrect_command = False
        if text == 'help' or text == 'помощь' or text == '/start' or text == '/help' or text == 'начать':
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Мои функции:' + '\n' +
                                      '- напишите мне "Отправить" для автоматической рассылки новостей, далее ' +
                                      'следуйте моим указаниям' + '\n' +
                                      '- напишите мне "Привет", и я поздороваюсь с Вами',
                              keyboard=base)
            incorrect_command = False
        if incorrect_command:
            vko.messages.send(user_id=event.user_id,
                              random_id=random.randint(1, 10 ** 9),
                              message='Извините, я Вас не понимаю. ' + '\n' +
                                      'Мои функции:' + '\n' +
                                      '- напишите мне "Отправить" для автоматической рассылки новостей, ' +
                                      'далее следуйте моим указаниям' + '\n' +
                                      '- напишите мне "Привет", и я поздороваюсь с Вами',
                              keyboard=base)
    # except Exception as er:
    #    print(er)
    #    pass
