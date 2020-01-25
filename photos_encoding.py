import glob
import pickle

import face_recognition


if __name__ == "__main__":
    known_faces_encodings = {}

    for i in glob.glob("base_of_photos/*.jpg"):
        photo = face_recognition.load_image_file(i)
        tmp = face_recognition.face_encodings(photo)
        if tmp != []:
            known_faces_encodings[i] = tmp[0]

    pickle.dump(known_faces_encodings, open("photos_prepared_for_face_recognition.dat", "wb"))

additional_p = 1
