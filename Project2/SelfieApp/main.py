#To run: In Terminal, go to CS4900/Project2/SelfieApp , and type in `python3 main.py`. To quit, press q.
#Authors: Trevor and Luke

import face_recognition
import cv2
import numpy as np

from gtts import gTTS
import pygame

# Initialize Video Capture
video_capture = cv2.VideoCapture(0)

# Initialize Face Classifier
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Face Classifier / Bounding Box code
def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 4))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)

        #Detect 4 Corners
        quadrant = detect4Corners(x, y, vid.shape[1], vid.shape[0])
                
        # Prints Quadrant
        cv2.putText(vid, f"Quadrant: {quadrant}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
    return faces

# Draw Quadrants Function
def quadrants(video_frame):
    height, width, _ = video_frame.shape
    centerX = width // 2
    centerY = height // 2
    X1 = width // 3
    Y1 = height // 4
    X2 = width - X1
    Y2 = height - Y1
    cv2.line(video_frame, (centerX, 0), (centerX, height), (0, 0, 255), 2) # Vertical Line
    cv2.line(video_frame, (0, centerY), (width, centerY), (0, 0, 255), 2) # Horizontal Line
    cv2.line(video_frame, (X1, Y1), (X1, Y2), (255, 0, 0), 2) # Center Left Line
    cv2.line(video_frame, (X1, Y1), (X2, Y1), (255, 0, 0), 2) # Center Top Line
    cv2.line(video_frame, (X2, Y1), (X2, Y2), (255, 0, 0), 2) # Center Right Line
    cv2.line(video_frame, (X1, Y2), (X2, Y2), (255, 0, 0), 2) # Center Bottom Line
    return video_frame

# Detect which corner quadrant bounding box is in
def detect4Corners(faceCenterX, faceCenterY, width, height):
    
    # Box detects what quadran its in
        if faceCenterX < width // 2 and faceCenterY < height // 2:
            return "Top Left"
        elif faceCenterX < width // 2 and faceCenterY > height // 2:
            return "Bottom Left"
        elif faceCenterX > width // 2 and faceCenterY < height // 2:
            return "Top Right"
        elif faceCenterX > width // 2 and faceCenterY > height // 2:
            return "Bottom Right"
        else:
            return "Center"


# Runs the Video Capture
while True:

    # This controls if video capture is active
    result, video_frame = video_capture.read()  
    if result is False:
        break  

    # Draw quadrants on screen
    video_frame = quadrants(video_frame)

    # Activeates bounding box while video capture is on
    faces = detect_bounding_box(video_frame)
    cv2.imshow("", video_frame)

    # Press 'q' to end the video capture
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release Resources
video_capture.release()
cv2.destroyAllWindows()