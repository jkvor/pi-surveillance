## About

A simple motion-based Raspberry Pi surveillance system.

## Hardware

* [Raspberry Pi](http://www.amazon.com/gp/product/B009SQQF9C)
* [Breadboard](http://www.amazon.com/gp/product/B004RXKWDQ)
* [Breakout kit](http://www.amazon.com/gp/product/B00EBXP3R2)
* [PIR sensor](http://www.amazon.com/gp/product/B007XQRKD4)
* [Camera board](http://www.amazon.com/gp/product/B00E1GGE40)

Breadboard configuration:

![](http://learn.adafruit.com/system/assets/assets/000/003/929/original/breadboard.png)

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
```

Clone repository and test:

```
$ git clone git@github.com:JacobVorreuter/pi-surveillance.git
$ cd pi-surrveillance
$ sudo -E ./motion_detector.py
```

Install upstart config and start daemon:

```
$ sudo cp motion-detector.conf /etc/init/
$ sudo start motion-detector
```

## Web client

[s3-image-viewer](https://github.com/JacobVorreuter/s3-image-viewer)
