import math

from djitellopy import tello
import KeyPressModule as kp
import cv2
import time
import numpy as np

#######################Parameters#####################
# Experiment values
fSpeed = 117 / 10  # Forward speed in cm/s (15cm/s)
aSpeed = 360 / 10  # Angular speed in Degrees/s (50deg/s)
interval = 0.25

dInterval = fSpeed * interval
aInterval = aSpeed * interval
######################################################
x, y = 500, 500
angle = 0
yaw = 0

trajectory = [(0, 0), (0, 0)]

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    angularSpeed = 50
    global x, y, yaw, angle  # Declare these variables as global
    distance = 0

    if kp.getKey("LEFT"):
        lr = -speed
        distance = dInterval
        angle = -180

    elif kp.getKey("RIGHT"):
        lr = speed
        distance = -dInterval
        angle = 180

    if kp.getKey("UP"):
        fb = speed
        distance = dInterval
        angle = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        distance = -dInterval
        angle = -90

    if kp.getKey("z"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("q"):
        yv = -angularSpeed
        yaw -= aInterval
    elif kp.getKey("d"):
        yv = angularSpeed
        yaw += aInterval

    if kp.getKey("SPACE"):
        me.takeoff()
    elif kp.getKey("RETURN"):
        me.land()

    time.sleep(interval)
    angle += yaw
    x += int(distance * math.cos(math.radians(angle)))
    y += int(distance * math.sin(math.radians(angle)))
    return [lr, fb, ud, yv, x, y]


def drawPoints(image, traj):
    for point in traj:
        cv2.circle(image, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(image, traj[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(image, f'({(traj[-1][0] - 500 )/ 100},{(traj[-1][1] - 500 )/ 100})m',
                (traj[-1][0] + 10, traj[-1][1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 1)


while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = np.zeros((1000, 1000, 3), np.uint8)
    if trajectory[-1][0] != vals[4] or trajectory[-1][1] != vals[5]:
        trajectory.append((vals[4], vals[5]))
    drawPoints(img, trajectory)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
