#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import site
site.addsitedir(
    "/Users/zomi/anaconda/lib/python2.7/site-packages/")
# ========================================================================
# How to run these script: $ /usr/bin/python main.py
# ========================================================================
import json
import os
import sys

import wx
import cv2
import numpy as np
from wx.lib import buttons

from core.utils import Stack
from core.framedata import get_label_data
from core.imgpprocess import SaveImage

FLOOD_VALUE = 15


class LeftPanel(wx.Panel):
    """
    The left panel object.
    # ==========================================
    # == Initialisation and Window Management ==
    # ==========================================
    """
    BMP_SIZE = 16
    BMP_BORDER = 3
    NUM_COLS = 4
    SPACING = 4
    LABEL_HINT = ["Classify Color", "Floodfill Range", "Brush Thickness"]

    def __init__(self, parent, ID, sketch):
        wx.Panel.__init__(self, parent, ID, style=wx.RAISED_BORDER)

        # Default parament
        self.sketch = sketch

        colorGrid = self.createColorGrid(parent)
        floodGrid = self.createFloodGrid(parent)
        # thickGrid = self.createThickGrid(parent)

        colorlabel = self.createLabelText(parent, self.LABEL_HINT[0])
        floodlabel = self.createLabelText(parent, self.LABEL_HINT[1])
        # thicklabel = self.createLabelText(parent, self.LABEL_HINT[2])

        self.layout(colorlabel, colorGrid, floodlabel, floodGrid)

    def createColorGrid(self, parent):
        buttonSize = (self.BMP_SIZE + 2 * self.BMP_BORDER,
                      self.BMP_SIZE + 2 * self.BMP_BORDER)

        self.label_data = get_label_data()
        self.show_label = self.label_data[0]['cn_name']
        self.curr_label = self.label_data[0]['en_name']
        self.curr_color = self.label_data[0]['color']
        self.colorMap = {}
        self.colorButtons = {}

        colorGrid = wx.GridSizer(cols=self.NUM_COLS, hgap=4, vgap=4)
        for idx, each_label in enumerate(self.label_data):
            color_rgb = tuple(each_label['color'])
            bmp = self._MakeBitmap(color_rgb)
            b = buttons.GenBitmapToggleButton(self, -1, bmp, size=buttonSize)
            b.SetBezelWidth(1)
            b.SetUseFocusIndicator(False)
            b.SetLabel(each_label['en_name'])
            self.Bind(wx.EVT_BUTTON, self.OnSetColour, b)
            colorGrid.Add(b, 0)
            self.colorMap[b.GetId()] = idx
            self.colorButtons[idx] = b
        self.colorButtons[0].SetToggle(True)

        return colorGrid

    def createThickGrid(self, parent):
        pass

    def createFloodGrid(self, parent):
        flood_grid = wx.GridSizer(rows=1, cols=1, hgap=0, vgap=0)
        self.slider = wx.Slider(self, -1, FLOOD_VALUE, 5, 40, pos=(0, 0), size=(100, -1),
                                style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.Bind(wx.EVT_SLIDER, self.OnSetFlood, self.slider)
        flood_grid.Add(self.slider, 0)

        return flood_grid

    def createLabelText(self, parent, label_text):
        labelGrid = wx.GridSizer(1, hgap=0, vgap=0)
        labeltext = wx.StaticText(parent, -1, label_text, (0, 0))
        labelGrid.Add(labeltext, 0)
        return labelGrid

    def OnSetColour(self, event):
        idx = self.colorMap[event.GetId()]
        self.curr_color = tuple(self.label_data[idx]['color'])
        self.show_label = self.label_data[idx]['cn_name']
        self.curr_label = self.label_data[idx]['en_name']

        print('Select [{}], color: {}'.format(
            self.curr_label, self.curr_color))

        if self.curr_color != self.sketch.innerPanel.color:
            # Set all the colorButtons Toggle to False
            for i in xrange(0, len(self.colorButtons)):
                self.colorButtons[i].SetToggle(False)
            self.colorButtons[idx].SetToggle(True)

        self.sketch.innerPanel.SetColor(self.curr_color)

    def OnSetFlood(self, event):
        flood_value = self.slider.GetValue()
        self.sketch.innerPanel.SetFloodValue(flood_value)
        print('Set flood value: {}'.format(flood_value))

    def OnSetThick(self, event):
        pass

    def _MakeBitmap(self, color_rgb):
        bmp = wx.EmptyBitmap(15, 15)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)

        brush = wx.Brush(wx.Colour(color_rgb[0], color_rgb[1], color_rgb[2]))
        dc.SetBackground(brush)
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)
        return bmp

    def layout(self, *Grid):
        box = wx.BoxSizer(wx.VERTICAL)

        for grid in Grid:
            box.Add(grid, 0, wx.ALL, self.SPACING)

        self.SetSizer(box)
        box.Fit(self)


class RightPanel(wx.Window):
    """
    The right panel object.
    # ==========================================
    # == Initialisation and Window Management ==
    # ==========================================
    """

    def __init__(self, parent, ID, img):
        wx.Window.__init__(self, parent, ID)
        self.SetBackgroundColour("Dark Grey")

        self.img = img
        self.innerPanel = DrawPanel(self, ID, self.img)

        # Align innerPanel in Center
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        innerBox = wx.BoxSizer(wx.VERTICAL)
        self.innerPanel.SetSizer(innerBox)
        hbox.Add(self.innerPanel, 0, wx.ALL | wx.ALIGN_CENTER)
        vbox.Add(hbox, 1, wx.ALL | wx.ALIGN_CENTER, 5)
        self.SetSizer(vbox)
        vbox.Fit(self)

    def OnLeftDown(self, event):
        self.pos = event.GetPositionTuple()
        self.CaptureMouse()

    def OnLeftUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
        self.Refresh()

    def OnMotion(self, event):
        pass

    def OnSize(self, event):
        pass

    def up_date(self):
        # when resieve an new image then update the panel.
        self.Update()


class DrawPanel(wx.Panel):
    """
    The draw panel object.
    # ==========================================
    # == Initialisation and Window Management ==
    # ==========================================
    """

    def __init__(self, parent, ID, img):
        draw_size = (900, 439)
        wx.Panel.__init__(self, parent, ID, size=draw_size)
        self.SetBackgroundColour("White")

        self.img = img
        self.floodmin_v = FLOOD_VALUE
        self.floodmax_v = FLOOD_VALUE
        maxpqueue = 10
        maxnqueue = 5

        # setup for floodFill
        self.stack_pre = Stack()
        self.stack_nex = Stack()

        self.label_data = get_label_data()
        self.color = tuple(self.label_data[0]['color'])
        self.floodmin = (self.floodmin_v,) * 3
        self.floodmax = (self.floodmax_v,) * 3
        height, width = self.img.shape[:2]
        self.mask = np.zeros((height + 2, width + 2), np.uint8)
        self.mask[:] = 0

        # setup for drawbitmap
        frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.bmp = wx.BitmapFromBuffer(width, height, frame)

        # Bind for event
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def OnLeftDown(self, event):
        self.dragline = []
        self.stack_pre.push(np.array(self.img))

        self.pos = event.GetPositionTuple()
        self.CaptureMouse()

    def OnLeftUp(self, event):
        if self.HasCapture():
            coords = (0, 0) + self.pos
            self.dragline.append(coords)
            self.ChangeFloodFill(coords)
            self.dragline = []
            self.ReleaseMouse()
        self.stack_nex.push(np.array(self.img))
        self.Refresh()

    def OnMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            self.DragMotion(event)
        event.Skip()

    def DragMotion(self, event):
        newPos = event.GetPositionTuple()
        coords = self.pos + newPos
        self.dragline.append(coords)
        self.ChangeFloodFill(coords)
        self.pos = newPos
        self.Refresh()

    def ChangeFloodFill(self, coords):
        # begin floodfill
        fill_color = (self.color[2], self.color[1], self.color[0])
        cv2.floodFill(self.img, self.mask, (coords[2], coords[3]),
                      fill_color, self.floodmin, self.floodmax)
        frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)

        print "[ACTION] floodfill {} with {}".format(self.pos, self.color)

    def SetColor(self, color_rgb):
        self.color = color_rgb

    def SetFillColor(self, color_rgb):
        self.color = color_rgb

    def SetBrushColor(self, color_rgb):
        self.brush_color = color_rgb
        self.pen = wx.Pen(self.brush_color, self.brush_thick, wx.SOLID)

    def SetFloodValue(self, flood_value):
        self.floodmin = (flood_value,) * 3
        self.floodmax = (flood_value,) * 3

    def SetBrushThick(self, num):
        self.brush_thick = num
        self.pen = wx.Pen(self.brush_color, self.brush_thick, wx.SOLID)

    def GetPre(self):
        # Mark: canot used the self.img save into Stack() because the numpy # is store in the memory, so we should deep copy the numpy like:
        # B = np.array(A)
        pre_img = self.stack_pre.pop()
        self.img = np.array(pre_img)
        frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()

    def GetNext(self):
        next_img = self.stack_nex.pop()
        self.img = np.array(next_img)
        frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()

    def next_iamge(self, img):
        self.img = np.array(img)
        frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()

    def save_image(self):
        print("[Save] Saving image...")
        save = SaveImage(self.img)
