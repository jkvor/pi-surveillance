http://learn.adafruit.com/system/assets/assets/000/003/929/original/breadboard.png?1360755758

```
$ sudo apt-get install upstart
$ sudo apt-get install python-dev
$ sudo apt-get install python-rpi.gpio
$ sudo cp motion-detector.conf /etc/init/
$ sudo start motion-detector
```

```
$ sudo -E ./motion_detector.py
```
