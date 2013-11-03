#!/usr/bin/python

import time, os, sys, subprocess
import s3_image_uploader
import RPi.GPIO as io

io.setmode(io.BCM)
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0) # reopen stdout in unbuffered mode

pir_pin = 18
io.setup(pir_pin, io.IN) # activate input

s3_bucket_name = os.environ['S3_IMAGE_UPLOADER_BUCKET_NAME']

def snap_photo():
    print("PIR ALARM: " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    cmd = "raspistill -w 828 -h 614 -q 20 -t 1000 -n -o -"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print "uploading image of size " + str(len(out))
    s3_image_uploader.upload(s3_bucket_name, s3_image_uploader.generate_image_name(), out)

# allow photo at:
# time 0
# time 10
# time 60
# time 300
# reset after 600
def is_throttled(last_activity, backoff):
    time_diff = (int(time.time()) - last_activity) 
    if time_diff > 600:
        backoff = 0

    print "backoff=" + str(backoff) + " time_diff=" + str(time_diff)
    if backoff == 0 and time_diff > 0:
        return (False, 10)
    elif backoff == 10 and time_diff > 10:
        return (False, 60)
    elif backoff == 60 and time_diff > 60:
        return (False, 300)
    elif backoff == 300 and time_diff > 300:
        return (False, 300)
    else:
        return (True, backoff)        

print "starting loop"
last_activity = 0
backoff = 0
while True:
    if io.input(pir_pin):
        (throttled, backoff) = is_throttled(last_activity, backoff)
        if not throttled:
            snap_photo()
	    last_activity = int(time.time())
    time.sleep(0.5)

