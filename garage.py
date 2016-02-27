#!/usr/bin/env python                                                                                                          
import time                                                                                                         
import RPi.GPIO as GPIO                                                                                                        
                                                                                                                             
GPIO.setmode(GPIO.BCM)                                                                                                         
GPIO.setwarnings(False)

hallActive = False                                                                                                             
topSensorTripped = False
doorOpen = False
bottomSensorTripped = False
doorCLosed = False
                                                                                                                               
OpenSensorTop = 23
ClosedSensorBottom = 17

GPIO.setup(OpenSensorTop, GPIO.IN)
GPIO.setup(ClosedSensorBottom, GPIO.IN)
top_time_stamp = time.time()
bottom_time_stamp = time.time()

def topMagnet(channel):
  global top_time_stamp
  global topSensorTripped
  global doorOpen
  global doorClosed
  top_time_now = time.time()

  if (GPIO.input(OpenSensorTop) == False) and ((top_time_now - top_time_stamp) >= 0.3):
    print("Top Sensor Triggered GPIO 23, Falling Edge")
    # If bottom is already tripped and now top is, means door is at limit open, if bottom isn't then we set topSensor true
    if (bottomSensorTripped):
      doorOpen = True
      doorClosed = False
    else:
      topSensorTripped = True
  else:
    print("Top Sensor did something?")

  top_time_stamp = top_time_now

def bottomMagnet(channel):
  global bottom_time_stamp
  global bottomSensorTripped
  global doorOpen
  global doorClosed
  bottom_time_now = time.time()

  if (GPIO.input(ClosedSensorBottom) == False) and ((bottom_time_now - bottom_time_stamp) >= 0.2):
    print("Bottom Sensor Triggered GPIO 17, Falling Edge")
    # if top is already tripped and now bottom is, means door is at limit closed, if top isn't then we set bottomSensor true
    if (topSensorTripped):
      doorClosed = True
      doorOpen = False
    else:
      bottomSensorTripped = True
  else:
    print("Bottom Sensor did something?")

  bottom_time_stamp = bottom_time_now

raw_input("Press Enter when ready\n>")

# Wait for a falling or rising edge from the hall sensor before executing the code below
# GPIO.wait_for_edge(OpenSensorTop, GPIO.FALLING)
GPIO.add_event_detect(OpenSensorTop, GPIO.FALLING, callback=topMagnet)
GPIO.add_event_detect(ClosedSensorBottom, GPIO.FALLING, callback=bottomMagnet)

# Main loop

print("Check for Top or Bottom Magnet")

while True:

#  if GPIO.input(ClosedSensorBottom):
#    doorClosing = GPIO.input(ClosedSensorBottom)
#    print("Yep, door near bottom rail, status is ", doorClosing)

  time.sleep(0.01)

GPIO.cleanup()

