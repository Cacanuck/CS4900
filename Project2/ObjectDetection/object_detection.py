import cv2
from ultralytics import YOLO

from gtts import gTTS
import os

# Load the model
yolo = YOLO('yolov8s.pt')

# Load the video capture
videoCap = cv2.VideoCapture(0)

# Function to get class colors
def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] * 
    (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)

# Function to draw quadrants and center box
def draw_quadrants(frame):
    height, width, _ = frame.shape
    centerX = width // 2
    centerY = height // 2
    X1 = width // 3
    Y1 = height // 4
    X2 = width - X1
    Y2 = height - Y1

    # Draw central lines
    cv2.line(frame, (centerX, 0), (centerX, height), (0, 0, 255), 2)  # Vertical Line
    cv2.line(frame, (0, centerY), (width, centerY), (0, 0, 255), 2)  # Horizontal Line

    # Draw center box
    cv2.rectangle(frame, (X1, Y1), (X2, Y2), (255, 0, 0), 2)  # Center Box

    return X1, Y1, X2, Y2, frame

# Function to determine the quadrant or center of the object
def get_object_region(x1, y1, x2, y2, X1, Y1, X2, Y2, width, height):
    # Get the center of the bounding box
    obj_center_x = (x1 + x2) // 2
    obj_center_y = (y1 + y2) // 2

    # If the object is within the center box, return "Center"
    if X1 <= obj_center_x <= X2 and Y1 <= obj_center_y <= Y2:
        return "Center"

    # Define the quadrants based on the center of the frame
    centerX, centerY = width // 2, height // 2
    if x1 <= centerX and y1 <= centerY:
        return "Top-left"
    elif x1 > centerX and y1 <= centerY:
        return "Top-right"
    elif x1 <= centerX and y1 > centerY:
        return "Bottom-left"
    elif x1 > centerX and y1 > centerY:
        return "Bottom-right"
    
    return "Unknown"

while True:
    ret, frame = videoCap.read()
    if not ret:
        continue
    results = yolo.track(frame, stream=True)

    # Draw the quadrants and center box
    X1, Y1, X2, Y2, frame = draw_quadrants(frame)

    for result in results:
        # Get the class names
        classes_names = result.names

        # Iterate over each box
        for box in result.boxes:
            # Check if confidence is greater than 40 percent
            if box.conf[0] > 0.4:
                # Get coordinates
                [x1, y1, x2, y2] = box.xyxy[0]
                # Convert to int
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Get the class
                cls = int(box.cls[0])

                # Get the class name
                class_name = classes_names[cls]

                # Get the respective color
                colour = getColours(cls)

                # Draw the rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)

                # Put the class name and confidence on the image
                cv2.putText(frame, f'{classes_names[cls]} {box.conf[0]:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)

                # Get the region the object is in and display it
                region = get_object_region(x1, y1, x2, y2, X1, Y1, X2, Y2, frame.shape[1], frame.shape[0])
                cv2.putText(frame, region, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                
    # Show the image
    cv2.imshow('frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and destroy all windows
videoCap.release()
cv2.destroyAllWindows()
