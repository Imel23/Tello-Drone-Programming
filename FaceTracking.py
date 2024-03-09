import time
import cv2
import numpy as np
from djitellopy import tello

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()
me.takeoff()
me.send_rc_control(0, 0, 25, 0)
time.sleep(1)
me.send_rc_control(0, 0, 0, 0)

w, h = 360, 240
fbRange = [6200, 6800]  # Forward and Backward Range
pid = [0.4, 0.4, 0]
pError = 0


def findFace(image):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListCenter = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(image, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListCenter.append([cx, cy])
        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:
        idx = myFaceListArea.index(max(myFaceListArea))
        return image, [myFaceListCenter[idx], myFaceListArea[idx]]
    else:
        return image, [[0, 0], 0]


def trackFace(me, info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20
    if x == 0:
        speed = 0
        error = 0
    me.send_rc_control(0, fb, 0, speed)
    return error


while True:
    img = me.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(me, info, w, pid, pError)
    print("Area:", info[1], "Center", info[0])
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break

