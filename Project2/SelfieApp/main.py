#To run: In Terminal, go to CS4900/Project2/SelfieApp , and type in `python3 main.py`. To quit, press q.
#Authors: Trevor and Luke

import face_recognition
import cv2
import numpy as np

video_capture = cv2.VideoCapture(0)

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 4))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces
    
while True:

    result, video_frame = video_capture.read()  
    if result is False:
        break  

    faces = detect_bounding_box(video_frame)
    cv2.imshow("", video_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()