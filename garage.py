#!/usr/bin/env python                                                                                                          
import time
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

topSensorTripped = False
doorOpen = False
bottomSensorTripped = False
doorClosed = False

OpenSensorTop = 23
ClosedSensorBottom = 17
GaragePower = 18

GPIO.setup(GaragePower, GPIO.OUT)
GPIO.setup(OpenSensorTop, GPIO.IN)
GPIO.setup(ClosedSensorBottom, GPIO.IN)

top_time_stamp = time.time()
bottom_time_stamp = time.time()


def moveDoor():
    GPIO.output(GaragePower,1)
    time.sleep(2)
    GPIO.output(GaragePower,0)
    time.sleep(2)
    GPIO.output(GaragePower,1)


def topMagnet(channel):
    global top_time_stamp
    global topSensorTripped
    global doorOpen
    global doorClosed
    top_time_now = time.time()
    if (GPIO.input(OpenSensorTop) == False) and ((top_time_now - top_time_stamp) >= 0.3):
        print("Top Sensor Triggered GPIO 23, Falling Edge")
        # If bottom is already tripped and now top, door is at limit open, if bottom isn't then we set topSensor true
        if (bottomSensorTripped):
            doorOpen = True
            doorClosed = False
            print("The Garage Door is Open!")
        else:
            topSensorTripped = True
            print("The Garage Door is Closing...")
    top_time_stamp = top_time_now


def bottomMagnet(channel):
    global bottom_time_stamp
    global bottomSensorTripped
    global doorOpen
    global doorClosed
    bottom_time_now = time.time()
    if (GPIO.input(ClosedSensorBottom) == False) and ((bottom_time_now - bottom_time_stamp) >= 0.2):
        print("Bottom Sensor Triggered GPIO 17, Falling Edge")
        # if top is already tripped and now bottom, door is at limit closed, if top isn't then we set bottomSensor true
        if (topSensorTripped):
            doorClosed = True
            doorOpen = False
            print("The Garage Door is Closed!")
        else:
            bottomSensorTripped = True
            print("The Garage Door is Opening...")
    bottom_time_stamp = bottom_time_now


# We could use: GPIO.wait_for_edge(OpenSensorTop, GPIO.FALLING), but need to watch both sensors concurrently
GPIO.add_event_detect(OpenSensorTop, GPIO.FALLING, callback=topMagnet)
GPIO.add_event_detect(ClosedSensorBottom, GPIO.FALLING, callback=bottomMagnet)


try:
    param = sys.argv[1]
except:
    param = 'none'

print("Parameter: %r" % param)
if param == "init":
    print("Start the motor and move the door...")
    moveDoor()
else:
    raw_input("Press Enter when ready to move the door>")
    moveDoor()


# Main loop
try:

    while not doorOpen or not doorClosed:
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
