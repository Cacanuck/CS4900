#To run: In Terminal, go to CS4900/Project2/SelfieApp , and type in `python3 main.py`. To quit, press q.
#Authors: Trevor and Luke

import face_recognition
import cv2
import numpy as np
import speech_recognition as sr

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

        # Calculate Face Center
        faceCenterX = x + w // 2
        faceCenterY = y + h // 2
        
        #Detect 4 Corners
        quadrant = detect4Corners(x, y, vid.shape[1], vid.shape[0])
        center = detectCenterBox(x, y, vid.shape[1], vid.shape[0])
        
        #Combine Quadrant and Center
        combined = f"{center}, {quadrant}" if quadrant != "None" else center
                
        # Prints Face Position
        cv2.putText(vid, f"Position: {combined}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
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
            return "None"

# Detect Center Box
def detectCenterBox(faceCenterX, faceCenterY, width, height):
    X1 = width // 3
    Y1 = height // 4
    X2 = width - X1
    Y2 = height - Y1
    
    if faceCenterX > X1 and faceCenterX < X2 and faceCenterY > Y1 and faceCenterY < Y2:
        return "Center"
    else:
        return "Not Centered"
    
# Get User Speech
def userInput():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            
            # Compensate for Background Noise
            recognizer.adjust_for_ambient_noise(source)
            
            # Get Input
            inputAudio = recognizer.listen(source)
            
            # Google Speech Recognition
            inputCommand = recognizer.recognize_google(inputAudio)
            return inputCommand.lower()
        
        except sr.UnknownValueError:
            # Play an error message could not understand audio
        except sr.RequestError:
            # Play speech recognition service error
        return None
    
# Take Screenshot
def screenshot(video_frame):
    screenshotPath = "screenshot.jpg"
    cv2.imwrite(screenshotPath, video_frame)
    return screenshotPath
    
# Runs the Video Capture
while True:

    # User Command to Take Picture
    input = userInput()
    if input:
        if "take picture" in input:
            screenShot = video_frame.copy()
            screenShot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
            screenshot(screenShot)
            continue
        
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