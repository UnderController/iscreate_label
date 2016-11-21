#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import site
site.addsitedir(
    "/Users/zomi/anaconda/lib/python2.7/site-packages/")
#=========================================================================
# HERE INCLUDE all the imge pre process program here.
#=========================================================================
import os
import sys
import json
import cv2
import wx
import numpy as np

from core.framedata import get_label_data


def WaterMark(img, alpha):
    """
    Trun input image into transparent image.

    @img: input image
    @aplha: transparent parament
    """
    (h, w) = img.shape[:2]
    # dstack add one col in the mat
    img = np.dstack([img, np.ones((h, w), dtype="uint8") * 255])
    overlay = np.zeros((h, w, 4), dtype="uint8")
    overlay[:, :, :] = 255  # whole image into white as cover layer

    dst = img.copy()
    cv2.addWeighted(overlay, alpha, dst, 1.0, 0, dst)
    return dst


def EqualizeHistColor(img, eq_type='yuv'):
    """
    Equalied image using histogram statical information. There are serical
    type can used in here.

    @type: yuv / rgb / gray
    """
    if eq_type == 'yuv':
        # equalize YUV - Y channel make the image more brightly.
        sp_img = cv2.split(img)
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        dst = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    elif eq_type == 'rgb':
        # equalize RGB three channel
        sp_img = cv2.split(img)
        dst = np.zeros((img.shape[0], img.shape[1], 3), dtype="uint8")
        for c in xrange(0, 3):
            dst[:, :, c] = cv2.equalizeHist(img[:, :, c])
    else:
        # qualize the gray iamge.
        dst = cv2.equalizeHist(img)

    return dst


def ColorReduce(img, div=64):
    """
    Reduce the color image from 256 * 256 * 256 into 4 * 4 * 4

    @img: input image
    @div: 255/div color
    """
    (h, w) = img.shape[:2]
    dst = np.zeros((img.shape[0], img.shape[1], 3), dtype="uint8")

    for c in xrange(0, img.shape[2]):
        dst[:, :, c] = img[:, :, c] / div * div + div / 2

    return dst


def AutoCannyColor(img, stype=1, parameter=0.65):
    """
    accroding to whole image gray value to set the canny parameter.

    @img: input image
    @parameter: canny threshold1 and threshold2 parameter, be symmetric.
    """
    canny = np.zeros(img.shape, dtype="uint8")

    if stype == 3:
        # used rgb will give more detail from the image -- recommand.
        sp_img = cv2.split(img)
        new_canny = []

        for idx, c in enumerate(sp_img):
            mu = np.mean(c)
            th1 = mu * parameter
            th2 = mu * parameter * 2
            img = cv2.Canny(c, th1, th2)
            new_canny.append(img)
        dst = cv2.cvtColor(cv2.merge(new_canny), cv2.COLOR_BGR2GRAY)
        ret, canny = cv2.threshold(dst, 10, 255, cv2.THRESH_BINARY)
    elif stype == 1:
        # can used by rgb and gray for fast auto canny.
        mu = np.mean(img)
        th1 = mu * parameter
        th2 = mu * parameter * 2
        canny = cv2.Canny(img, th1, th2)
    else:
        pass

    return canny


def BlurImage(img, btype='median', ks=5):
    """
    By experience the best blue method is GaussianBlur with kernel size 5.

    @img: input image
    @btype: gauss / median / normal
    @ks: kernel size
    """
    if btype == 'normal':
        dst = cv2.blur(img, (ks, ks))
    elif btype == 'median':
        dst = cv2.medianBlur(img, ks)
    elif btype == 'gauss':
        dst = cv2.GaussianBlur(img, (ks, ks), 0)
    else:
        pass

    return dst


def ResizeImage(img, div, width=None):
    """
    Resize the orginal image.

    @img: imput image
    @div: reduce size of orginal image
    @width: if have width and no div.
    """
    (h, w) = [float(x) for x in list(img.shape[:2])]

    if div > 0:
        dst = cv2.resize(img, (w / div, h / div))
        return dst

    div = img.shape[0] / float(width)
    dst = cv2.resize(img, (w / div, h / div))
    return dst


class PreProcess(object):
    """
    Vital task: run before laod the image from the images list. Group1 is test
    by experience, group2 and group3 is waitting for completion.

    TODO: bine the watermark image with canny outline in C++.
    """

    def __init__(self, img):
        super(PreProcess, self).__init__()
        self.org_img = img
        self.group1()

    def group1(self):
        '''
        step1: get canny outline by orginal image.
        step2: reduce the color into 32 in the orginal image.
        step3: transparent the reduce color image into 0.8.
        step4: combine the transparent image with canny outline.
        '''
        # self.hist_img = EqualizeHistColor(self.org_img)

        self.blur = BlurImage(self.org_img, btype='normal', ks=3)
        self.canny = AutoCannyColor(self.blur, stype=1)
        # cv2.imshow("canny", self.canny)
        # cv2.imwrite("_test_canny.jpg", self.canny)

        self.blur = BlurImage(self.org_img, btype='normal', ks=3)
        self.reduce = ColorReduce(self.blur, div=32)
        # cv2.imshow("reduce", self.reduce)
        # cv2.imwrite("_test_reduce.jpg", self.reduce)

        self.red_dst = WaterMark(self.reduce, 0.2)
        # cv2.imshow("red_dst", self.red_dst)
        # cv2.imwrite("_test_red_dst.jpg", self.red_dst)

        # combine the watermark image with canny outline

        cv2.waitKey(0)

    def group2(self):
        '''
        step1:
        step2:
        step3:
        step4:
        '''
        pass

    def group3(self):
        '''
        step1:
        step2:
        step3:
        step4:
        '''
        pass


class SaveImage(object):
    """
    Vital task: run after saving the image.

    TODO: used C++ to change the PNG image with some aplha piexl and canny line.
    """

    def __init__(self, img):
        super(SaveImage, self).__init__()
        self.img = img
        label_data = get_label_data()
        self.label_color = []
        for idx, each_label in enumerate(label_data):
            self.label_color.append(each_label['color'])

        self.run()

    def run(self):
        self.write()

    def show(self):
        cv2.imshow("test", self.img)
        cv2.waitKey(0)

    def write(self):
        cv2.imwrite("save.png", self.img)
