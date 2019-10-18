import glob

import face_recognition

known_faces_encodings = {}


for i in glob.glob("base_of_photos/*.jpg"):
    photo = face_recognition.load_image_file(i)
    #print(face_recognition.face_encodings(photo))
    if not face_recognition.face_encodings(photo) == []:
        known_faces_encodings[i] = face_recognition.face_encodings(photo)[0]
