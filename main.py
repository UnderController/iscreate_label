#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ========================================================================
# How to run these script: $ /usr/bin/python main.py
# ========================================================================

try:
    import wx
except:
    import site
    site.addsitedir("/Users/zomi/anaconda/lib/python2.7/site-packages/")
    import wx
import os
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
        self.size = (1100, 750)
        self.style = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent, id, self.title,
                          size=self.size, style=self.style)

        # setup parament
        self.img_idx = 0
        self.tool = "magic"
        self.tool_iconsize = [20, 20]
        self.img_list = read_images()
        self.img_path = self.img_list[self.img_idx]
        self.beg_img = cv2.imread(self._check_label_img(self.img_path))  # BGR

        # main Panel
        self.sketch = MagicPanel(
            self, -1, self.beg_img, self.img_path, self.tool)

        # self.initMenuBar()
        self.initStatusBar()
        self.initToolBar()
        self.createPanel()

    def _check_label_img(self, org_path):
        path, name = os.path.split(org_path)
        nname = os.path.splitext(name)
        new_path = os.path.join(path, nname[0] + '_L.png')
        if os.path.isfile(new_path):
            return new_path
        else:
            return org_path

    def createPanel(self):
        self.leftPanel = LeftPanel(self, -1, self.sketch, self.tool)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.leftPanel, 0, wx.EXPAND)
        box.Add(self.sketch, 1, wx.EXPAND)
        self.SetSizerAndFit(box)  # WARNING:

        # Bind
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyPressed)
        wx.EVT_MOTION(self.leftPanel, self.OnMotion)

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
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])

    def OnMotion(self, event):
        self.statusbar.SetStatusText(
            "Classify: {} - {}".format(
                self.leftPanel.show_label.encode('utf-8'),
                self.leftPanel.curr_label), 0)
        self.statusbar.SetStatusText(
            "Tool: {}".format(self.tool), 1)
        self.statusbar.SetStatusText(
            "Color: {}".format(self.leftPanel.curr_color), 2)
        event.Skip()

    def _toolBarIconData(self):
        """
        Toolbar icon info is store in here. TODO: change into json or XML file.
        """
        toolBarIconList = (
            # ('New', 'icons/new_20.png',
            #     'Open New Image File.', self.OnNew),
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
        print("[ToolBar] New: open new file")

    def OnSave(self, event):
        print("[ToolBar] Save: save img file")
        self.sketch.innerPanel.save_image()

    def OnMagic(self, event):
        # used floodfill method fill range color in the graphy
        if not self.tool == "magic":
            self.tool = "magic"

            img = self.sketch.innerPanel.img.copy()
            color = self.sketch.innerPanel.get_color()
            self.sketch.Destroy()
            self.leftPanel.Destroy()
            self.sketch = MagicPanel(self, -1, img, self.img_path, self.tool)
            self.sketch.innerPanel.set_color(color)
            # self.leftPanel.Update()
            self.createPanel()
            self.Refresh()
            event.Skip()
            print("[ToolBar] Brush: Using magic wand")
        else:
            print("[ToolBar] Brush: Already magic wand")
            event.Skip()

    def OnBrush(self, event):
        # use brush to draw line and point in the graphy
        if not self.tool == "brush":
            self.tool = "brush"

            img = self.sketch.innerPanel.img.copy()
            color = self.sketch.innerPanel.get_color()
            self.sketch.Destroy()
            self.leftPanel.Destroy()
            self.sketch = BrushPanel(self, -1, img, self.img_path, self.tool)
            self.sketch.innerPanel.set_color(color)
            self.createPanel()
            self.Refresh()
            event.Skip()
            print("[ToolBar] Brush: Using brush pen")
        else:
            print("[ToolBar] Brush: Already brush pen")
            event.Skip()

    def OnPolygon(self, event):
        self.tool = "Polygon"
        print("[ToolBar] Polygon: Polygon tool is not finish.")

    def OnColor(self, event):
        dialog = wx.ColourDialog(None)
        dialog.GetColourData().SetChooseFull(True)
        if dialog.ShowModal() == wx.ID_OK:
            colour_data = dialog.GetColourData()
            curr_color = colour_data.GetColour().Get()
            self.leftPanel.curr_color = curr_color
            self.sketch.innerPanel.set_color(curr_color)

        print("[ToolBar] Color: Select Color {} From Panel".format(
            str(colour_data.GetColour().Get())))
        dialog.Destroy()

    def OnForward(self, event):
        if not self.sketch.innerPanel.stack_nex.is_empty():
            self.sketch.innerPanel.GetNext()
            print("[ToolBar] Next: go to next step")
        else:
            print("[ToolBar] Next: next stack is empty")

    def OnBackward(self, event):
        if not self.sketch.innerPanel.stack_pre.is_empty():
            self.sketch.innerPanel.get_pre()
            print("[ToolBar] Pre: previous step")
        else:
            print("[ToolBar] Pre: pre stack is empty")

    def OnNextImg(self, event):
        # TODO: at the end of next iamge should open a new dialog
        # warm user it is the end of images list. Mark confirm and
        # exit.
        self.img_idx += 1
        if self.img_idx < len(self.img_list):
            nimg_path = self.img_list[self.img_idx]
            new_img = cv2.imread(self._check_label_img(nimg_path))
            color = self.sketch.innerPanel.get_color()
            self.sketch.innerPanel.save_image()

            print("[ToolBar] Next: Go to next image: {}".format(nimg_path))
            self.sketch.innerPanel.next_iamge(new_img, nimg_path)
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
