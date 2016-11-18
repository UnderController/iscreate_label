#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import site
site.addsitedir(
    "/Users/zomi/anaconda/lib/python2.7/site-packages/")
# ====================================================================================
# How to run these script: $ /usr/bin/python main.py
# ====================================================================================
import os
import wx
import cv2

from panel import *
from core.utils import scale_bitmap
from core.framedata import read_images

class CreateTool():
    pass


class TopFrame(wx.Frame):
    """
    A frame showing the contents of a single document.
    # ==========================================
    # == Initialisation and Window Management ==
    # ==========================================
    """

    def __init__(self, parent=None, id=-1):
        """ Standard constructor.

            'parent', 'id' and 'title' are all passed to the standard wx.Frame
            constructor.  'fileName' is the name and path of a saved file to
            load into this frame, if any.
        """

        self.title = "Label Tools -- iscreate"
        self.size = (1000, 730)
        self.style = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent, id, self.title,
                          size=self.size, style=self.style)

        self.img_idx = 0
        self.img_list = read_images()
        img_path = self.img_list[self.img_idx]
        new_img = cv2.imread(img_path)

        self.sketch = RightPanel(self, -1, new_img)
        self.tool_iconsize = [20, 20]
        # self.initMenuBar()
        self.initStatusBar()
        self.initToolBar()
        self.createPanel()

        # Bind
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyPressed)
        wx.EVT_MOTION(self.leftPanel, self.OnMotion)


    def createPanel(self):
        self.leftPanel = LeftPanel(self, -1, self.sketch)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.leftPanel, 0, wx.EXPAND)
        box.Add(self.sketch, 1, wx.EXPAND)
        self.SetSizer(box)

    def initToolBar(self):
        toolbar = self.CreateToolBar()
        toolbar.SetToolBitmapSize(tuple(self.tool_iconsize))

        for eachtool in self._toolBarIconData():
            self.createFrameTool(toolbar, *eachtool)
        toolbar.AddSeparator()

        toolbar.Realize()

    def createFrameTool(self, toolbar, label, filename, help, handler):
        # Check not add separator
        if not label:
            toolbar.AddSeparator()
            return

        # bmp = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bitmap = wx.Bitmap(filename)
        bitmap = scale_bitmap(bitmap, self.tool_iconsize)

        tool = toolbar.AddSimpleTool(-1, bitmap, label, help)
        self.Bind(wx.EVT_MENU, handler, tool)

    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-1, -1])

    def OnMotion(self, event):
        self.statusbar.SetStatusText(
            "分类: {} - {}".format(self.leftPanel.show_label.encode('utf-8'), self.leftPanel.curr_label), 0)
        self.statusbar.SetStatusText(
            "Color: {}".format(self.leftPanel.curr_color), 1)
        event.Skip()

    def _toolBarIconData(self):
        """
        Toolbar icon info is store in here. TODO: change into json or XML file.
        """
        toolBarIconList = (
            ('New', 'icons/new_20.png',
                'Open New Image File.', self.OnNew),
            ('Save', 'icons/save_20.png',
                'Save current image file.', self.OnSave),
            ('Next', 'icons/next_20.png',
                'Next image.', self.OnNextImg),
            ("", "", "", ""),
            ('Magic', 'icons/magic_20.png',
                'Use magic wand.', self.OnMagic),
            ('Brush', 'icons/brush_20.png',
                'Use brush pen.', self.OnBrush),
            ('Polygon', 'icons/polygon_20.png',
                'Use polygon point.', self.OnPolygon),
            ('Color', 'icons/color_20.png',
                'Select Color From Panel.', self.OnColor),
            ("", "", "", ""),
            ('Forward', 'icons/forward_20.png',
                'Goto preview step', self.OnForward),
            ('Backward', 'icons/backward_20.png',
                'Goto next step', self.OnBackward),
        )

        # Incase the running python dir is not in the environment.
        # toolBarIconList_ = []
        # for toolIcon in toolBarIconList:
        #     toolIcon_ = list(toolIcon)
        #     if not toolIcon_[0]:
        #         continue
        #     iconname = os.path.join(os.getcwd(), toolIcon_[1])
        #     toolIcon_[1] = iconname
        #     toolBarIconList_.append(tuple(toolIcon_))
        # return tuple(toolBarIconList_)

        return toolBarIconList

    def OnNew(self, event):
        print "[ToolBar] New: {}".format("open new file")

    def OnSave(self, event):
        print("[ToolBar] Save: save img file")
        self.sketch.innerPanel.save_image()

    def OnMagic(self, event):
        print "[ToolBar] Magic: {}".format("Use magic wand")

    def OnBrush(self, event):
        print "[ToolBar] Brush: {}".format("Use brush pen")

    def OnPolygon(self, event):
        print "[ToolBar] Polygon: {}".format("Use polygon point")

    def OnColor(self, event):
        dialog = wx.ColourDialog(None)
        dialog.GetColourData().SetChooseFull(True)
        if dialog.ShowModal() == wx.ID_OK:
            colour_data = dialog.GetColourData()
            curr_color = colour_data.GetColour().Get()
            self.leftPanel.curr_color = curr_color
            self.sketch.innerPanel.SetColor(curr_color)

        print("[ToolBar] Color: Select Color {} From Panel".format(
            str(colour_data.GetColour().Get())))
        dialog.Destroy()

    def OnForward(self, event):
        if not self.sketch.innerPanel.stack_nex.is_empty():
            self.sketch.innerPanel.GetNext()
            print("[ToolBar] Next: go to next step")

    def OnBackward(self, event):
        if not self.sketch.innerPanel.stack_pre.is_empty():
            self.sketch.innerPanel.GetPre()
            print("[ToolBar] Pre: {} back to preview step")

    def OnNextImg(self, event):
        # TODO: at the end of next iamge should open a new dialog
        # warm user it is the end of images list. Mark confirm and
        # exit.
        self.img_idx += 1
        if self.img_idx < len(self.img_list):
            nimg_path = self.img_list[self.img_idx]
            new_img = cv2.imread(nimg_path)

            print("[ToolBar] Next: Go to next image: {}".format(nimg_path))
            self.sketch.innerPanel.save_image()
            self.sketch.innerPanel.next_iamge(new_img)
        else:
            print("[Exit] No more iamges.")
            self.sketch.innerPanel.save_image()
            self.OnCloseWindow(event)

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnKeyPressed(self, event):
        if event.GetKeyCode() == 81:
            self.sketch.innerPanel.save_image()
            self.Destroy()
        else:
            event.Skip()


class LabelApp(wx.App):
    """
    The main application object.
    # ==========================================
    # == Initialisation and Window Management ==
    # ==========================================
    """

    def __init__(self, redirect=False, filename=None):
        print "Label App __init__"
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        """
         Initialise the application.
        """
        print "OnInit"

        self.frame = TopFrame(None, -1)
        self.frame.Centre()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)

        return True

if __name__ == '__main__':
    app = LabelApp(redirect=False)
    print "beging Main Loop"
    app.MainLoop()
    print "After Main Loop"
