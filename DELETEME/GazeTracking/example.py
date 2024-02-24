"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import chime
import cv2
import keyboard
import time
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

global calibration_flag
global blinkHold
global caliZone
cailbrationPoints = list()
caliZone = 0
blinkhold = 0
calibration_flag = False


def run_a():
    global caliZone
    global cailbrationPoints
    global calibration_flag

    calibration_flag = True

    print("Calibrating... Press 'a' and keep your eyes fixed on a point.")
    
    # Reset calibration points
    tempCaliPoints = []

    # Collect eye coordinates for 10 frames
    for _ in range(50):
        _, frame = webcam.read()
        gaze.refresh(frame)
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        tempCaliPoints.append((left_pupil, right_pupil))

    leftSum = 0
    leftCount = 0
    rightSum = 0
    rightCount = 0
    for points in tempCaliPoints:
        for point in points:
            if point[0] is not None:
                leftSum += point[0]
                leftCount += 1
            if point[1] is not None:
                rightSum += point[1]
                rightCount += 1
    avgLeft = int(leftSum/leftCount)
    avgRight = int(rightSum/rightCount)
    print("(" + str(avgLeft) + ", " + str(avgRight) + ")")

    calibration_flag = False
    caliZone += 1
    cailbrationPoints.append(tempCaliPoints)
    print("Calibration complete. Eye coordinates recorded.")
    print("Calibration Points:", tempCaliPoints)
    

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
        blinkhold += 1
        if blinkhold >= 10:
            text = "Eyes Closed"
            blinkhold = 0
            ##chime.success()
    elif gaze.is_right():
        text = "Looking right"
        blinkhold = 0
    elif gaze.is_left():
        text = "Looking left"
        blinkhold = 0
    elif gaze.is_center():
        text = "Looking center"
        blinkhold = 0

    if keyboard.is_pressed("a") and not calibration_flag:
        run_a()


    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
