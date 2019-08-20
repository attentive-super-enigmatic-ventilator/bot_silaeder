import face_recognition
import glob

known_faces_encodings = dict()

for i in glob.glob("/home/alexandr/PycharmProjects/chatbot/photos_base/*.jpg"):
    photo = face_recognition.load_image_file(i)
    #print(face_recognition.face_encodings(photo))
    if not face_recognition.face_encodings(photo) == []:
        known_faces_encodings[i] = face_recognition.face_encodings(photo)[0]
