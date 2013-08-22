# -*- coding:utf-8 -*-
import wx
import wx.richtext as rt

# This event class and binder object can be used to catch
# notifications that the ExpandoTextCtrl has resized itself and
# that layout adjustments may need to be made.
wxEVT_ETC_LAYOUT_NEEDED = wx.NewEventType()
EVT_ETC_LAYOUT_NEEDED = wx.PyEventBinder( wxEVT_ETC_LAYOUT_NEEDED, 1 )

class MyRichTextCtrl(rt.RichTextCtrl):
    def __init__(self, parent, pos = wx.DefaultPosition, numLines = 6):
        rt.RichTextCtrl.__init__(self, parent, -1, pos=pos, style = wx.BORDER_NONE)

        DefaultFont = wx.Font(13,
                              wx.FONTFAMILY_DEFAULT,
                              wx.FONTSTYLE_NORMAL,
                              wx.FONTWEIGHT_NORMAL,
                              face=u"微软雅黑")

        self.SetFont(DefaultFont)

        self.SetFocus()
        self.SetFocusFromKbd()

        self.charHeight = self.GetCharHeight()
        self.linespacing = 3
        self.upsapceing = 4
        self.downspacing = 20

        self.numLines = numLines
        height = self.upsapceing + numLines * self.charHeight + \
                 (numLines - 1)*self.linespacing + self.downspacing
        self.SetSize((200, height))
        self.SetMinSize((200, height))


        self.Bind(wx.EVT_TEXT, self.OnTextChanged)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnTextChanged(self, evt):
        # check if any adjustments are needed on every text update
        self._adjustCtrl()
        evt.Skip()

    def OnSize(self, evt):
        # The number of lines needed can change when the ctrl is resized too.
        self._adjustCtrl()
        evt.Skip()

    def _adjustCtrl(self):
        nlines = self.GetNumberOfLines()

        if nlines >= self.numLines:
            height = self.upsapceing + nlines * self.charHeight + \
                     (nlines - 1)*self.linespacing + self.downspacing

            if self.GetContainingSizer() is not None:
                mw, mh = self.GetMinSize()
                self.SetMinSize((mw, height))
                if self.GetParent().GetSizer() is not None:
                    self.GetParent().Layout()
                else:
                    self.GetContainingSizer().Layout()
            else:
                self.SetSize((-1, height))

            # send notification that layout is needed
            evt = wx.PyCommandEvent(wxEVT_ETC_LAYOUT_NEEDED, self.GetId())
            evt.SetEventObject(self)
            evt.height = height
            evt.numLines = nlines
            self.GetEventHandler().ProcessEvent(evt)

    def GetNumberOfLines(self):
        text = self.GetValue()
        width = self.GetSize().width
        dc = wx.ClientDC(self)
        dc.SetFont(self.GetFont())
        count = 0
        for line in text.split('\n'):
            count += 1
            w, h = dc.GetTextExtent(line)
            if w > width:
                # the width of the text is wider than the control,
                # calc how many lines it will be wrapped to
                count += self._wrapLine(line, dc, width)

        if not count:
            count = 1
        return count

    def _wrapLine(self, line, dc, width):
        # Estimate where the control will wrap the lines and
        # return the count of extra lines needed.
        pte = dc.GetPartialTextExtents(line)
        width -= wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
        idx = 0
        start = 0
        count = 0
        spc = -1
        while idx < len(pte):
            if line[idx] == ' ':
                spc = idx
            if pte[idx] - start > width:
                # we've reached the max width, add a new line
                count += 1
                # did we see a space? if so restart the count at that pos
                if spc != -1:
                    idx = spc + 1
                    spc = -1
                start = pte[idx]
            else:
                idx += 1
        return count


class RichTextFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1,
                    style = wx.BORDER_NONE
                          | wx.FRAME_NO_TASKBAR
                          | wx.STAY_ON_TOP)

        self.SetSize((500, 500))
        self.SetPosition((100, 100))

        self.rtc = rtc = MyRichTextCtrl(self);
        wx.CallAfter(self.rtc.SetFocus)



if __name__ == '__main__':
    app = wx.App(False)
    frame = RichTextFrame(None)
    frame.Show(True)
    app.MainLoop()