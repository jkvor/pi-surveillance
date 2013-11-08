#!/usr/bin/python

import time, os, sys, subprocess
import s3_image_uploader
import RPi.GPIO as io

io.setmode(io.BCM)
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0) # reopen stdout in unbuffered mode

pir_pin = 18
io.setup(pir_pin, io.IN) # activate input

s3_bucket_name = os.environ['S3_IMAGE_UPLOADER_BUCKET_NAME']
image_width = int(os.environ['S3_IMAGE_WIDTH'])

def snap_photos(num_photos):
    photos = []
    while num_photos > 0:
        photos.append(snap_photo())
	num_photos = num_photos - 1
    for (filename, contents) in photos:
	print "uploading image, " + filename + ", of size " + str(len(contents))
	s3_image_uploader.upload(s3_bucket_name, filename, contents)

def snap_photo():
    cmd = "raspistill -w " + str(image_width) + " -h " + str(int(image_width / 1.3333)) + " -q 20 -t 1000 -n -o -"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return (s3_image_uploader.generate_image_name(), out)

# allow photo at:
# time 0 (3x)
# time 10
# time 60
# time 300
# reset after 600
# returns (num_photos_to_take, new_backoff)
def is_throttled(last_activity, backoff):
    time_diff = (int(time.time()) - last_activity) 
    if time_diff > 600:
        backoff = 0

    print "backoff=" + str(backoff) + " time_diff=" + str(time_diff)
    if backoff == 0 and time_diff > 0:
        return (3, 10)
    elif backoff == 10 and time_diff > 10:
        return (1, 60)
    elif backoff == 60 and time_diff > 60:
        return (1, 300)
    elif backoff == 300 and time_diff > 300:
        return (1, 300)
    else:
        return (0, backoff)        

print "starting loop"
last_activity = 0
backoff = 0
while True:
    if io.input(pir_pin):
        (num_photos, backoff) = is_throttled(last_activity, backoff)
        if num_photos > 0:
	    last_activity = int(time.time())
	    print("PIR ALARM: " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
            snap_photos(num_photos)
    time.sleep(0.5)

