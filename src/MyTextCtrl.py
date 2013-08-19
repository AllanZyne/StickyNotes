import wx
from wx.lib.expando import ExpandoTextCtrl

StaticText = wx.StaticText

wxEVT_ETC_LAYOUT_NEEDED = wx.NewEventType()
EVT_ETC_LAYOUT_NEEDED = wx.PyEventBinder( wxEVT_ETC_LAYOUT_NEEDED, 1 )

class MyTextCtrl(ExpandoTextCtrl):
    def __init__(self, parent, pos=wx.DefaultPosition,  size=wx.DefaultSize):
        ExpandoTextCtrl.__init__(self, parent, pos = pos, size = size, style = wx.BORDER_NONE)
        self.SetMinSize(size)

    def _adjustCtrl(self):
        numLines = self.GetNumberOfLines()
        if numLines != self.numLines:
            self.numLines = numLines
            charHeight = self.GetCharHeight()

            print "numLimes:", numLines
            print "charHeight:", charHeight
            print "extraHeight:", self.extraHeight

            height = numLines * charHeight + self.extraHeight
            if numLines > 2:
                height += (numLines - 2)*5

            print "cur_height: ", height
            print "size:", self.GetSize()

            if not (height < self.MinHeight):
                if not (self.maxHeight != -1 and height > self.maxHeight):
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
                    evt.numLines = numLines
                    self.GetEventHandler().ProcessEvent(evt)