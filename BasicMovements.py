from djitellopy import tello
from time import sleep


me = tello.Tello()
me.connect()
print(me.get_battery())

me.takeoff()
# Move forward by controlling speed
me.send_rc_control(0, 30, 0, 0)
sleep(2)

# Move right by controlling speed
me.send_rc_control(30, 0, 0, 0)
sleep(2)

# Rotate by controlling speed
me.send_rc_control(0, 0, 0, 30)
sleep(2)

# Stop drone before landing
me.send_rc_control(0, 0, 0, 0)
me.land()
