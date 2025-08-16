import cv2
import face_recognition
import mysql.connector
import numpy as np
def connect_db():
    return mysql.connector.connect(host="localhost", user="root",password="root",database="face_db")

def get_registered_faces():
    conn= connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, encoding FROM faces")
    data=cursor.fetchall()
    conn.close()

    known_face_names=[]
    known_face_encodings=[]

    for name, encoding in data:
        known_face_names.append(name)
    known_face_encodings.append(np.frombuffer(encoding, dtype=np.float64))
    return known_face_names, known_face_encodings

def log_recognition(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs(name) VALUES(%s)",(name,))
    conn.commit()
    conn.close()


def recognize_face():
    known_face_names, known_face_encodings= get_registered_faces()
    cap= cv2.VideoCapture(0)
    ret,frame=cap.read()
    cap.release()

    if not ret:
        print("Failed to capture image")
        return
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    face_locations= face_recognition.face_locations(rgb_frame, face_locations)
    for face_encoding in face_encoding:
        matches=face_recognition.compare_faces(known_face_encodings,face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches [best_match_index] :
                name=known_face_names[best_match_index]
                log_recognition(name)
                print(f"Recognized:{name}")
            else:
              print("Unknown face")
        else:
            print("No known faces found")
    recognize_face()
