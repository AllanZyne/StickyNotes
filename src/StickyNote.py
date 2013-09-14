# -*- coding:utf-8 -*-
import wx
# from MyTextCtrl import MyTextCtrl, EVT_ETC_LAYOUT_NEEDED
from MyRichTextCtrl import  MyRichTextCtrl, EVT_ETC_LAYOUT_NEEDED
from MyPanel import MyPanel

class StickyNote(wx.Control):
    '''
        We simply derive a new class of Frame.
    '''

    def __init__(self, parent, pos = wx.DefaultPosition, size = wx.DefaultSize):
        self.MySize = MySize = (224, 163)
        self.delta = (0,0)

        wx.Control.__init__(self, parent, -1, pos = pos, size = size,
                    style = wx.BORDER_NONE
                          | wx.FRAME_NO_TASKBAR
                          | wx.STAY_ON_TOP)

        # Make a VBOXSIZER
        box = wx.BoxSizer(wx.VERTICAL)
        self.sizer = box

        # MAKE A PANEL
        pnl = MyPanel(self) #, size = (224, 35))
        box.Add(pnl, 0, wx.EXPAND)
        self.panel = pnl

        # MAKE A TEXT CONTROL
        tc = MyRichTextCtrl(self)
        box.Add(tc, 1, wx.EXPAND)
        self.text_control = tc

        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit)

        self.SetSizer(box)

        self.SetTheme("yellow")

        self.Pinned(True)
        self.LockPos(False)
        self.LockEdit(False)

        self.sizer.Fit(self)
        self.Fit()

        self.Show(True)


    def OnRefit(self, evt):
        self.sizer.Fit(self)
        self.Fit()

    def Exit(self):
        print "StickyNotes.OnExit()"
        self.Close()

    def Pinned(self, status = False):
        self.hasPinned = status

        flag = self.GetWindowStyleFlag()
        if status:
            flag = flag | wx.STAY_ON_TOP
        else:
            flag = flag & (~ wx.STAY_ON_TOP)
        self.SetWindowStyleFlag(flag)

    def LockPos(self, status):
        self.hasLockPos = status
        if not status:
            self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            self.panel.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            self.panel.Bind(wx.EVT_MOTION, self.OnMouseMove)
        else:
            self.panel.Unbind(wx.EVT_LEFT_DOWN)
            self.panel.Unbind(wx.EVT_LEFT_UP)
            self.panel.Unbind(wx.EVT_MOTION)

            self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown2)
            self.panel.Bind(wx.EVT_LEFT_UP, self.OnLeftUp2)
            self.panel.Bind(wx.EVT_MOTION, self.OnMouseMove2)

    def LockEdit(self, status):
        self.hasLockEdit = status
        if status:
            self.text_control.SetEditable(False)
        else:
            self.text_control.SetEditable(True)

    def OnLeftDown2(self, evt):
        evt.Skip()

    def OnLeftUp2(self, evt):
        self.text_control.SetFocus()
        evt.Skip()

    def OnMouseMove2(self, evt):
        self.text_control.SetFocus()
        evt.Skip()

    def OnLeftDown(self, evt):
        x, y = self.ClientToScreen(evt.GetPosition())
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))


    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)


    def SetTheme(self, color):
        yellow_theme = [wx.Colour(253, 251, 154), wx.Colour(252, 250, 175)]

        themes = { "yellow": yellow_theme }

        self.panel.SetBackgroundColour(themes[color][0])
        self.text_control.SetBackgroundColour(themes[color][1])

        pass

#
# app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
# frame = MyFrame(None, "Sticky Notes") # A Frame is a top-level window.
# frame.Show(True)     # Show the frame.
# app.MainLoop()
