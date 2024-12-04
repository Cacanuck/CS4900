# object_detection.py
# Authors: Trevor and Luke

# import classes
import cv2
from ultralytics import YOLO
from gtts import gTTS
import pygame
import os
import speech_recognition as sr
import time
import threading

# load the model
yolo = YOLO('yolov8s.pt')

# load the video capture
videoCap = cv2.VideoCapture(0)

# load the mixer for TTS
pygame.mixer.init()

# initialize global variables
current_quadrant = None
object_in_right_place = False
check_time = time.time()
picture_taken = False

# TTS sound functions
def play_select_object():
    pygame.mixer.music.load("selectObject.mp3")
    pygame.mixer.music.play()

def play_select_quadrant():
    pygame.mixer.music.load("selectQuadrant.mp3")
    pygame.mixer.music.play()

def play_move_up():
    pygame.mixer.music.load("moveObjectUp.mp3")
    pygame.mixer.music.play()

def play_move_down():
    pygame.mixer.music.load("moveObjectDown.mp3")
    pygame.mixer.music.play()

def play_move_left():
    pygame.mixer.music.load("moveObjectLeft.mp3")
    pygame.mixer.music.play()

def play_move_right():
    pygame.mixer.music.load("moveObjectRight.mp3")
    pygame.mixer.music.play()

def play_moveUpRight():
    pygame.mixer.music.load("moveUpRight.mp3")
    pygame.mixer.music.play()

def play_moveUpLeft():
    pygame.mixer.music.load("moveUpLeft.mp3")
    pygame.mixer.music.play()

def play_moveDownRight():
    pygame.mixer.music.load("moveDownRight.mp3")
    pygame.mixer.music.play()

def play_moveDownLeft():
    pygame.mixer.music.load("moveDownLeft.mp3")
    pygame.mixer.music.play()

def play_object_in_proper_quadrant():
    pygame.mixer.music.load("objectInProperQuadrant.mp3")
    pygame.mixer.music.play()

def play_pictureTaken():
    pygame.mixer.music.load("pictureTaken.mp3")
    pygame.mixer.music.play()

# get an object as input from the user
# code from geeksforgeeks speech to text guide
def recognize_object():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say the object you want to find.")
        audio = recognizer.listen(source)

        try:
            item = recognizer.recognize_google(audio)
            print(f"You said:", item)
            return item
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

# get the target quadrant from the user
# code from geeksforgeeks speech to text guide
def recognize_quadrant():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say the quadrant you wish the item to be in.")
        audio = recognizer.listen(source)

        try:
            quadrant = recognizer.recognize_google(audio)
            print(f"You said:", quadrant)
            quadrant = quadrant.strip().lower()
            return quadrant
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

# function to get class colors
# code from geeksforgeeks object detection with YOLO guide
def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] * 
    (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)

# function to draw quadrants and center box
# code from geeksforgeeks object detection with YOLO guide
def draw_quadrants(frame):
    height, width, _ = frame.shape
    centerX = width // 2
    centerY = height // 2
    X1 = width // 3
    Y1 = height // 4
    X2 = width - X1
    Y2 = height - Y1

    # draw central lines
    cv2.line(frame, (centerX, 0), (centerX, height), (0, 0, 255), 2)  # Vertical Line
    cv2.line(frame, (0, centerY), (width, centerY), (0, 0, 255), 2)  # Horizontal Line

    # draw center box
    cv2.rectangle(frame, (X1, Y1), (X2, Y2), (255, 0, 0), 2)  # Center Box

    return X1, Y1, X2, Y2, frame

# function to determine the quadrant or center of the object
def get_object_region(x1, y1, x2, y2, X1, Y1, X2, Y2, width, height):
    obj_center_x = (x1 + x2) // 2
    obj_center_y = (y1 + y2) // 2

    if X1 <= obj_center_x <= X2 and Y1 <= obj_center_y <= Y2:
        return "center"

    centerX, centerY = width // 2, height // 2
    if x1 <= centerX and y1 <= centerY:
        return "top left"
    elif x1 > centerX and y1 <= centerY:
        return "top right"
    elif x1 <= centerX and y1 > centerY:
        return "bottom left"
    elif x1 > centerX and y1 > centerY:
        return "bottom right"
    
    return "Unknown"

# function to find the object in the frame and execute the rest of the code if it
def check_for_object(target_item, target_quadrant):
    global current_quadrant, object_in_right_place, check_time, picture_taken
    while True:
        ret, frame = videoCap.read()
        if not ret:
            continue
        
        results = yolo.track(frame, stream=True)

        # draw the quadrants and center box
        # includes code from geeksforgeeks YOLO object detection
        X1, Y1, X2, Y2, frame = draw_quadrants(frame)
        found = False  # Flag to check if the object was found
        for result in results:
            classes_names = result.names

            for box in result.boxes:
                # check if confidence is greater than 40 percent
                if box.conf[0] > 0.4:
                    # get coordinates
                    [x1, y1, x2, y2] = box.xyxy[0]
                    # convert to int
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # get the class
                    cls = int(box.cls[0])

                    # get the class name
                    class_name = classes_names[cls]

                    # get the respective color
                    colour = getColours(cls)

                    # draw the rectangle
                    cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)

                    # get the region the object is in and display it
                    region = get_object_region(x1, y1, x2, y2, X1, Y1, X2, Y2, frame.shape[1], frame.shape[0])

                    current_quadrant = region

                    # if the class name matches the target item
                    if target_item in class_name.lower():
                        print(f"Found {class_name}!")
                        cv2.putText(frame, f"{class_name}: {region}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        found = True
                        break
            if found:
                break

        # check every 5 seconds if object is in the correct quadrant
        # includes code from geeksforgeeks time.time() guide and Timer Objects in Python guide
        if time.time() - check_time > 5:
            check_time = time.time()
            move_to_quadrant(current_quadrant, target_quadrant)

            if current_quadrant == target_quadrant and not object_in_right_place:
                print("Object is in the correct quadrant!")
                play_object_in_proper_quadrant()
                object_in_right_place = True
                start_time = time.time()

        if object_in_right_place:
            if time.time() - start_time >= 8 and not picture_taken:
                take_picture(frame)
                picture_taken = True

        cv2.imshow('frame', frame)

        # break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# give directions to move the item
def move_to_quadrant(current_quadrant, target_quadrant):
    if current_quadrant == target_quadrant:
        print("The object is already in the target quadrant.")
        return
    
    # determine directions
    if target_quadrant == "top left":
        if current_quadrant == "top right":
            play_move_left()
        elif current_quadrant == "bottom left":
            play_move_up()
        elif current_quadrant == "bottom right":
            play_moveUpLeft()
        elif current_quadrant == "center":
            play_moveUpLeft()
        else:
            print("Unknown quadrant combination.")
    
    elif target_quadrant == "top right":
        if current_quadrant == "top left":
            play_move_right()
        elif current_quadrant == "bottom left":
            play_moveUpRight()
        elif current_quadrant == "bottom right":
            play_move_up()
        elif current_quadrant == "center":
            play_moveUpRight()
        else:
            print("Unable to complete action")
    
    elif target_quadrant == "bottom left":
        if current_quadrant == "top left":
            play_move_down()
        elif current_quadrant == "top right":
            play_moveDownLeft()
        elif current_quadrant == "bottom right":
            play_move_left()
        elif current_quadrant == "center":
            play_moveDownLeft()
        else:
            print("Unable to complete action")
    
    elif target_quadrant == "bottom right":
        if current_quadrant == "top left":
            play_moveDownRight()
        elif current_quadrant == "top right":
            play_move_down()
        elif current_quadrant == "bottom left":
            play_move_right()
        elif current_quadrant == "center":
            play_moveDownRight()
        else:
            print("Unable to complete action")
    
    elif target_quadrant == "center":
        if current_quadrant == "top left":
            play_moveDownRight()
        elif current_quadrant == "top right":
            play_moveDownLeft()
        elif current_quadrant == "bottom left":
            play_moveUpRight()
        elif current_quadrant == "bottom right":
            play_moveUpLeft()
    
    else:
        print("Invalid target quadrant.")

# take the picture
def take_picture(frame):
    cv2.imwrite("my_picture.jpg", frame)
    play_pictureTaken()

# get the target item from the user
play_select_object()
target_item = recognize_object()

# get the target quadrant from the user
play_select_quadrant()
target_quadrant = recognize_quadrant()

# find the object and take the picture
if target_item:
    check_for_object(target_item, target_quadrant)  # Start object detection to find the item
else:
    print("No item recognized.")

# release the video capture and destroy all windows
videoCap.release()
cv2.destroyAllWindows()