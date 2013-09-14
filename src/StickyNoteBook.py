# -*- coding:utf-8 -*-
import os
import webbrowser
import wx
import wx.richtext as rt
import wx.lib.scrolledpanel as scrolled
import wx.lib.platebtn as platebtn

import StickyNote

class NoteWidget(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style = wx.BORDER_THEME)
        self.SetMinSize((-1, 300))
        self.SetBackgroundColour("white")

        title_edit = wx.TextCtrl(self)#, style = wx.BORDER_NONE)
        # title_edit.SetMinSize((-1, 30))
        content_edit = wx.TextCtrl(self, style = wx.BORDER_NONE | wx.TE_MULTILINE)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title_edit, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(content_edit, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title=title, size = (400, 400),
            style = wx.DEFAULT_FRAME_STYLE )

        StickyNoteBook(self)


class StickyNoteBook(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)

        # Layout
        self.__DoLayout()
        self.SetupScrolling()


    def __DoLayout(self):

        # w1 = StickyNote.StickyNote(self, pos=(50, 50))
        # w, h = self.GetClientSize()
        e1 = NoteWidget(self)
        # e2 = NoteWidget(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(e1, 1, wx.EXPAND | wx.ALL, 10)
        # sizer.Add(e2, 1, wx.EXPAND | wx.ALL, 10)
        # sizer.AddMany([(p1, 0, wx.EXPAND), (p2, 0, wx.EXPAND),
        #                (p3, 0, wx.EXPAND)])
        # hsizer = wx.BoxSizer(wx.HORIZONTAL)
        # hsizer.Add(sizer, 1, wx.EXPAND)
        self.SetSizer(sizer)
        # e1.GetSizer().Fit(self)
        sizer.Fit(self)

        # self.SetAutoLayout(True)


    def OnDropArrowPressed(self, evt):
        print "DROPARROW PRESSED"


    def OnChildFocus(self, evt):
        """Override ScrolledPanel.OnChildFocus to prevent erratic
        scrolling on wxMac.

        """
        if wx.Platform != '__WXMAC__':
            evt.Skip()

        child = evt.GetWindow()
        self.ScrollChildIntoView(child)


class GradientPanel(wx.Panel):
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent, size=size)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        col1 = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DSHADOW)
        col2 = platebtn.AdjustColour(col1, -90)
        col1 = platebtn.AdjustColour(col1, 90)
        rect = self.GetClientRect()
        grad = gc.CreateLinearGradientBrush(0, 1, 0, rect.height - 1, col2, col1)

        pen_col = tuple([min(190, x) for x in platebtn.AdjustColour(col1, -60)])
        gc.SetPen(gc.CreatePen(wx.Pen(pen_col, 1)))
        gc.SetBrush(grad)
        gc.DrawRectangle(0, 1, rect.width - 0.5, rect.height - 0.5)

        evt.Skip()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, "dfas")
    frame.Show(True)
    app.MainLoop()