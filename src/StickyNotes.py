import wx
from MyTextCtrl import MyTextCtrl, EVT_ETC_LAYOUT_NEEDED

class MyFrame(wx.Frame):
    '''
        We simply derive a new class of Frame.
    '''

    def __init__(self, parent, title):
        self.MySize = MySize = (224, 193)

        wx.Frame.__init__(self, parent, -1, title=title, size = MySize,
                          style = wx.BORDER_NONE | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

        self.delta = (0,0)
        yellow_theme = [wx.Colour(253, 251, 154), wx.Colour(252, 250, 175)]

        self.SetBackgroundColour(yellow_theme[0])

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_RIGHT_UP, self.OnExit)

        w, h = MySize
        self.text_ctrl = MyTextCtrl(self, size = (w, h - 30), pos = (0, 30))

        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit)
        # self.text_ctrl.SetScrollbar(0, 0, 0, 0)
        self.text_ctrl.SetBackgroundColour(yellow_theme[1])
        self.Show(True)

    def OnRefit(self, evt):
        print "refit called!!"
        self.SetSize((-1, evt.height + 30))
        self.
        # self.Fit()

    def OnExit(self, evt):
        self.Close()


    def OnLeftDown(self, evt):
        self.CaptureMouse()
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


app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = MyFrame(None, "Small editor") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()
