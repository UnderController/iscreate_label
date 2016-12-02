IsLabel
==============

[![Build Status](https://travis-ci.org/cvhciKIT/sloth.svg)](https://travis-ci.org/cvhciKIT/sloth)

IsLabel is a tool for labeling image and video data for computer vision research.

IsLabel's purpose is to provide a versatile tool for various labeling tasks in the context of computer vision research. Since there are so many different label formats and requirements out there, we concluded that is virtually impossible to build the one label tool sufficient to handle all labeling tasks. Therefore, this project can be seen rather as a framework and set of standard components to quickly configure a label tool specificly tailored to ones needs.

In this documentation we will go over some of the key concepts of IsLabel, how to configure IsLabel using the standard components provided in the package, and finally how to go further and write custom visualization items and label format containers to deal with specific labeling needs.

Input & Output
==============

Input image:

![Input](https://i.stack.imgur.com/L4ZXF.jpg)

Output image:

![Output](https://i.stack.imgur.com/ffKnC.png)

Install
========
Ubuntu 14.04 finish.

##Requirement##

```
$$ sudo apt-get opencv2
$$ sudo apt search python-wxgtk
$$ sudo apt-get install python-wxgtk3.0
$$ sudo pip install numpy
```

And then change the path of the input imagelist in /data/imagelist.txt

##Run##

```
ubuntu: python main.py
mac os: /usr/bin/python main.py
```

Temp
====

```
git ls-files --deleted -z | xargs -0 git rm 
find . -name "*.pyc" -print | xargs rm -rf 
git add -u
git add *
git commit -m "fix some bug"
git push origin master
```
