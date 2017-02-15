# Geospatial-Vision-and-Visualization
Geospatial Vision and Visualization - CS 513

# Using vagrant box

Basic commands

```bash
$ vagrant up # start
$ vagrant halt # stop
$ vagrant ssh # ssh into the box
```

## First run

First `vagrant up` will take a ton of time, so be prepared for that.

Once `vagrant up` completes for the first time, confirm that everything is installed properly by doing the following:

```
$ vagrant ssh
# ...
vagrant@vagrant-ubuntu-trusty-64:~$ workon cv
(cv) vagrant@vagrant-ubuntu-trusty-64:~$ python
Python 3.5.2 (default, Jul 17 2016, 00:00:00)
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> cv2.__version__
'3.1.0'
```

## Directory structure

You can access your currently mounted directory at `/vagrant`.
