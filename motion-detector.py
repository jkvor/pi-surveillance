#!/usr/bin/python

import time, os, sys
import RPi.GPIO as io
io.setmode(io.BCM)
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0) # reopen stdout in unbuffered mode

pir_pin = 18
io.setup(pir_pin, io.IN) # activate input

# os.environ['MOTION_DETECTOR_THROTTLE_WINDOW']
throttle_window = 10
last_activity = 0

print "starting loop"
while True:
    if (int(time.time()) - last_activity) > throttle_window:
        if io.input(pir_pin):
            print("PIR ALARM!")
	    last_activity = int(time.time())
    time.sleep(0.5)

