#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import site
site.addsitedir(
    "/Users/zomi/anaconda/lib/python2.7/site-packages/")
#-------------------------------------------------------------------------
# How to run these script: $ /usr/bin/python main.py
#-------------------------------------------------------------------------
import os
import sys
import json

import wx


def scale_bitmap(bitmap, wh_list):
    """
    Change to bitmap size from bitmap.Getsize to [w, h]
    """
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(wh_list[0], wh_list[1], wx.IMAGE_QUALITY_HIGH)
    bmp = wx.BitmapFromImage(image)
    return bmp


class EmptyStackError(Exception):
    def __init__(self, message="Stack is empty: cannot pop from an empty stack!"):
        self.message = message

class FullStackError(Exception):
    def __init__(self, message="Stack is full: cannot push to a full stack!"):
        self.message = message


class Stack(object):
    """docstring for Stack"""
    def __init__(self, max_size = 15):
        self.max_size = max_size
        self.data = []

    def is_empty(self):
        if len(self.data) == 0:
            return True

    def is_full(self):
        if len(self.data) == self.max_size:
            return True

    def push(self, value):
        if not self.is_full():
            self.data.append(value)
            # print "PUSH ==" * 10
            # print self.data
            return value
        else:
            self.pop()

    def pop(self):
        if not self.is_empty():
            out_value = self.data[len(self.data) - 1]
            del self.data[len(self.data) - 1]
            # print "POP ==" * 10
            # print self.data
            # print out_value
            return out_value
        else:
            raise EmptyStackError()



