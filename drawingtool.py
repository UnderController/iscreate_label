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


#============================================================================
class DrawingTool(object):
    """Base class for drawing tools"""

    def __init__(self):
        pass

    def getDefaultCursor(self):
        return wx.STANDARD_CURSOR

    def draw(self, dc):
        pass

    def onMouseEvent(self, parent, event):
        event.Skip()
        return False

#----------------------------------------------------------------------------
