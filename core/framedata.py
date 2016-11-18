#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import site
site.addsitedir(
    "/Users/zomi/anaconda/lib/python2.7/site-packages/")
#-------------------------------------------------------------------------
# How to run these script: $ /usr/bin/python main.py
#-------------------------------------------------------------------------
import wx
import os
import sys
import json

toolBarIconList = [
    ['New', 'icons/new_20.png',
     'Open New Image File.'],
    ['Save', 'icons/save_20.png',
     'Save current image file.'],
    ["", "", "", ""],
    ['Magic', 'icons/magic_20.png',
     'Use magic wand.'],
    ['Brush', 'icons/brush_20.png',
     'Use brush pen.'],
    ['Polygon', 'icons/polygon_20.png',
                'Use polygon point.'],
    ['Color', 'icons/color_20.png',
     'Select Color From Panel.'],
    ["", "", "", ""],
    ['Forward', 'icons/forward_20.png',
                'Goto preview step'],
    ['Backward', 'icons/backward_20.png',
     'Goto next step'],
]

def get_label_data(labelfile=None):
    """
    Get the Classify color list from the json file: labelname.json
    """
    if not labelfile:
        labelfile = "data/labelname.json"

    if not os.path.isfile(labelfile):
        sys.exit("[Error] Canot find label file: {}".format(labelfile))

    with open(labelfile, 'r') as f:
        label_data = json.load(f)
    return label_data


def read_images(image_path=None):
    """
    Get the iamge list from the file: imagelist.txt
    """
    if not image_path:
        image_path = "data/imagelist.txt"

    if not os.path.isfile(image_path):
        sys.exit("[Error] Canot find label file: {}".format(image_path))

    with open(image_path, 'r') as fs:
        content =  fs.readlines()
    content = [x.rstrip('\n') for x in content]
    return content


if __name__ == '__main__':
    data = read_images("../data/imagelist.txt")
    print data
