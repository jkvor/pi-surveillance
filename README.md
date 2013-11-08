## About

A simple motion-based Raspberry Pi surveillance system.

Read more about how the system works in [this blog post](http://www.jkvor.com/blog/2013/11/06/raspberry-pi-surveillance/).

## Raspberry Pi configuration

Install upstart to manage daemon process and python packages:

```
$ sudo apt-get install upstart
$ sudo apt-get install python-dev
$ sudo apt-get install python-rpi.gpio
```

Add the following config vars to `~/.profile`:

```
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export S3_IMAGE_UPLOADER_BUCKET_NAME=
export S3_IMAGE_WIDTH=
export PI_SURVEILLANCE_DIR=$HOME/dev/pi-surveillance
```

Clone repository and manually start daemon in foreground:

```
$ source ~/.profile
$ git clone git@github.com:JacobVorreuter/pi-surveillance.git $PI_SURVEILLANCE_DIR
$ cd $PI_SURVEILLANCE_DIR
$ sudo -E ./motion_detector.py
```

Install upstart config and daemon:

```
$ sudo cp motion-detector.conf /etc/init/
$ sudo start motion-detector
$ tail -f /tmp/motion-detector.log
```

## Web client

[s3-image-viewer](https://github.com/JacobVorreuter/s3-image-viewer)
