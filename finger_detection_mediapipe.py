import cv2
import mediapipe as mp
import pyautogui as pag
import math
import os
if os.name == 'posix':
    from Xlib import X, display
    from Xlib.ext.xtest import fake_input

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.5)

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera

#get screen width and length :
screen_width, screen_height = pag.size()

"""
Windows :
import ctypes

# Move the mouse
ctypes.windll.user32.SetCursorPos(int(screen_width - (landmark.x * screen_width)), int(landmark.y * screen_height))

# Click the mouse
ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up
"""
class Mouse:
    def __init__(self):
        # Platform specific code
            #Linux
            if os.name == 'posix':
                self.display = display.Display()

    def move(self, x, y):
        if os.name == 'posix':
            # Move the mouse
            fake_input(self.display, X.MotionNotify, x=x, y=y)
            self.display.sync()

    def click(self):
        if os.name == 'posix':
            # Click the mouse
            fake_input(self.display, X.ButtonPress, 1)
            self.display.sync()
            fake_input(self.display, X.ButtonRelease, 1)
            self.display.sync()

    def press(self):
        if os.name == 'posix':
            # Press the mouse
            fake_input(self.display, X.ButtonPress, 1)
            self.display.sync()

    def release(self):
        if os.name == 'posix':
            # Release the mouse
            fake_input(self.display, X.ButtonRelease, 1)
            self.display.sync()

            
mouse = Mouse()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands in the frame
    results = hands.process(frame_rgb)

    # If hands are detected, display landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for idx, landmark in enumerate(hand_landmarks.landmark):

                if idx == 8:
                    wrist = hand_landmarks.landmark[0]
                    middle_finger = hand_landmarks.landmark[12]

                    # Extract landmark positions
                    h, w, c = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    # Draw a circle on each landmark point
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                    #print(landmark.x * w, landmark.y * h)

                    hand_length = math.sqrt(abs(wrist.x * w - (middle_finger.x * w))**2 + abs(wrist.y * h - (middle_finger.y * h))**2)
                    distance = math.sqrt(abs(cx - (middle_finger.x * w))**2 + abs(cy - (middle_finger.y * h))**2)

                    print(f"distance: {distance}, hand_length: {hand_length}")
                    if hand_length >= 100.0: 
                        # move the mouse :
                        pag.moveTo(screen_width - (landmark.x * screen_width), landmark.y * screen_height, 0)

                        if distance < 30.0:
                            mouse.press()
                        else:
                            mouse.release()

                if idx == 12:
                    # Extract landmark positions
                    h, w, c = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    # Draw a circle on each landmark point
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
                    #print(landmark.x * w, landmark.y * h)


    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Display the frame
    cv2.imshow('Finger Detection', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
