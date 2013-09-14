# -*- coding:utf-8 -*-
import wx
import wx.richtext as rt

class MyRichTextFileHandler(rt.RichTextFileHandler):
    def __init__(self, name = wx.EmptyString, ext = wx.EmptyString, type = 0):
        self.name = name
        self.ext = ext
        self.type = type

    def CanHandle(self, filename):

        if self.name == filename:
            return True
        return False

    def CanLoad(self):
        return True



