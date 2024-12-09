#To run: In Terminal, go to CS4900/Project2/SelfieApp , and type in `python3 main.py`. To quit, press q.
#Authors: Trevor and Luke

import face_recognition
import cv2
import numpy as np
import speech_recognition as sr
import threading
import time
import queue

from gtts import gTTS
import pygame

# Initialize Video Capture
video_capture = cv2.VideoCapture(0)

# Initialize Face Classifier
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Initialize Audio Mixer
pygame.mixer.init()

# Queue For Speech Thread
speechQueue = queue.Queue()

# Flag to Check if Audio is Playing
audioPlaying = threading.Event()

# Timer for Detection in Quadrant
quadTimer = {"start": None, "position": False}

# Face Classifier / Bounding Box code
def detect_bounding_box(vid, selection):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 4))
    
    # Limit Speech Recognition
    lastCheck = time.time()
    interval = 10

    if time.time() - lastCheck > interval:
        selection
        lastCheck = time.time()     

    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        
        #Detect 4 Corners
        quadrant = detect4Corners(x, y, vid.shape[1], vid.shape[0])
        center = detectCenterBox(x, y, vid.shape[1], vid.shape[0])
        
        #Combine Quadrant and Center
        combined = f"{center}, {quadrant}" if quadrant != "None" else center
        
        # Prints Face Position
        cv2.putText(vid, f"Position: {combined}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Guide User to Selected Area
        if selection in ["center", "top left", "top right", "bottom left", "bottom right"]:
            position = guide(selection, vid, x,y,w,h)
            
            # Prompt User to Take Picture
            if position:
                playAudio("picture.mp3")
                position = False
                video_frame = clearLines(original)
                screenshot(video_frame)
                video_capture.release()
                video_capture = 0
                cv2.destroyAllWindows()
        
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
    
    # Box detects what quadrant its in
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
        
        # Adjust for Ambient Noise
        recognizer.adjust_for_ambient_noise(source)
        
        # Get Input
        inputAudio = recognizer.listen(source)
        
        try:
            
            # Google Speech Recognition
            inputCommand = recognizer.recognize_google(inputAudio)
            return inputCommand.lower()
        
        except sr.UnknownValueError:
            playAudio("notUnderstand.mp3")
            time.sleep(5)
        except sr.RequestError as e:
            playAudio("serviceError.mp3")
    
# Take Screenshot
def screenshot(video_frame):
    screenshotPath = "screenshot.jpg"
    time.sleep(3)
    cv2.imwrite(screenshotPath, video_frame)
    return screenshotPath

# Play an Audio File
def playAudio(file):
    def play():
        if audioPlaying.is_set():
            return
        
        audioPlaying.set()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        audioPlaying.clear()
        
    threading.Thread(target=play).start()
    
# Guide the User to the Correct Location
def guide(target, frame, x,y,w,h):
    faceCenterX = x + w // 2
    faceCenterY = y + h // 2
    height, width, _ = frame.shape
    global quadTimer
    
    # Timer calculation Setup
    currentTime = time.time()
    wait = 1.5
    
    # Reset Timer
    def resetTimer():
        quadTimer["start"] = None
        quadTimer["position"] = False
        
    # If User Wants Center
    if target == "center":
        if width // 3 < faceCenterX < width - width // 3 and height // 4 < faceCenterY < height - height // 4:
            if quadTimer["start"] is None:
                quadTimer["start"] = currentTime
            elif currentTime - quadTimer["start"] >= wait:
                quadTimer["position"] = True
                return True
        else:
            resetTimer()
            if faceCenterX < width // 3:
                playAudio("moveHeadLeft.mp3")
            elif faceCenterX > width - width // 3:
                playAudio("moveHeadRight.mp3")
            if faceCenterY < height // 4:
                playAudio("moveHeadDown.mp3")
            elif faceCenterY > height - height // 4:
                playAudio("moveHeadUp.mp3")

    # If User Wants A Quadrant
    else:
        if target == "top left":
            if faceCenterX < width // 2 and faceCenterY < height // 2:
                if quadTimer["start"] is None:
                    quadTimer["start"] = currentTime
                elif currentTime - quadTimer["start"] >= wait:
                    quadTimer["position"] = True
                    return True
            else:
                resetTimer()
                if faceCenterX >= width // 2:
                    playAudio("moveHeadRight.mp3")
                if faceCenterY >= height // 2:
                    playAudio("moveHeadUp.mp3")
        elif target == "top right":
            if faceCenterX > width //2 and faceCenterY < height // 2:
                if quadTimer["start"] is None:
                    quadTimer["start"] = currentTime
                elif currentTime - quadTimer["start"] >= wait:
                    quadTimer["position"] = True
                    return True
            else:
                resetTimer()
                if faceCenterX <= width // 2:
                    playAudio("moveHeadLeft.mp3")
                if faceCenterY >= height // 2:
                    playAudio("moveHeadUp.mp3")
        elif target == "bottom left":
            if faceCenterX < width // 2 and faceCenterY > height // 2:
                if quadTimer["start"] is None:
                    quadTimer["start"] = currentTime
                elif currentTime - quadTimer["start"] >= wait:
                    quadTimer["position"] = True
                    return True
            else:
                resetTimer()
                if faceCenterX >= width // 2:
                    playAudio("moveHeadRight.mp3")
                if faceCenterY <= height // 2:
                    playAudio("moveHeadDown.mp3")
        elif target == "bottom right":
            if faceCenterX > width // 2 and faceCenterY > height // 2:
                if quadTimer["start"] is None:
                    quadTimer["start"] = currentTime
                elif currentTime - quadTimer["start"] >= wait:
                    quadTimer["position"] = True
                    return True
            else:
                resetTimer()
                if faceCenterX <= width // 2:
                    playAudio("moveHeadLeft.mp3")
                if faceCenterY <= height // 2:
                    playAudio("moveHeadDown.mp3")
                    
    return False

# Clear Grid and Bounding Box Lines
def clearLines(original):
    return original

# Flag For Prompt To Play 1 Time
played = False
    
# Runs the Video Capture
while True:
        
    # This controls if video capture is active
    result, video_frame = video_capture.read()  
    if result is False:
        break  

    # Keep Original Frame for Line Deletion
    original = video_frame.copy()
    
    # Draw quadrants on screen
    video_frame = quadrants(video_frame)
    
    # Start Prompt
    if played == False:
        playAudio("prompt.mp3")
        selection = userInput()
        print("You Selected: ")
        print(selection)
        played = True    
    
    # Activeates bounding box while video capture is on
    faces = detect_bounding_box(video_frame, selection)
    
    # Display Video
    cv2.imshow("", video_frame)
        
    # Press 'q' to end the video capture
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release Resources
video_capture.release()
video_capture = 0
cv2.destroyAllWindows()