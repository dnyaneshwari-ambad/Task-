import cv2
import mysql.connector
import numpy as np

# Connect to MySQL Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="face_db"
)
cursor = db.cursor()

# Load OpenCV Face Detection Model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Open Webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        # Draw rectangle around detected faces
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Show the video feed
    cv2.imshow("Face Detection", frame)

    # Press 'c' to capture and save image
    key = cv2.waitKey(1)
    if key == ord("c"):
        name = input("Enter name: ")  # Get user input for name
        
        # Convert image to binary data
        _, img_encoded = cv2.imencode(".jpg", frame)
        img_bytes = img_encoded.tobytes()
        
        # Insert image into MySQL database
        query = "INSERT INTO Face (id,name, image) VALUES ( %s,%s,%s)"
        cursor.execute(query, (1,name, img_bytes))
        db.commit()
        
        print("Image saved successfully!")
    
    # Press 'q' to quit
    elif key == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
cursor.close()
db.close()