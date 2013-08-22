# -*- coding:utf-8 -*-
import wx
from wx.lib.expando import ExpandoTextCtrl

StaticText = wx.StaticText

wxEVT_ETC_LAYOUT_NEEDED = wx.NewEventType()
EVT_ETC_LAYOUT_NEEDED = wx.PyEventBinder( wxEVT_ETC_LAYOUT_NEEDED, 1 )

class MyTextCtrl(ExpandoTextCtrl):
    def __init__(self, parent, pos=wx.DefaultPosition):
        ExpandoTextCtrl.__init__(self, parent, pos = pos, style = wx.BORDER_NONE)

        # Set Font Syle
        self.SetFontStyle(fontColor=wx.Colour(0, 0, 0),
                          fontFace=u'微软雅黑',
                          fontSize=13,
                          fontBold=False, fontItalic=False, fontUnderline=False)

        # Set Height (8 lines)
        height = 8 * self.charHeight
        self.InitHeight = height
        self.SetMinSize((-1, self.InitHeight))
        self.SetSize((-1, self.InitHeight))

        self.SetFocus()


    def _adjustCtrl(self):
        numLines = self.GetNumberOfLines()
        if numLines != self.numLines:
            self.numLines = numLines
            charHeight = self.charHeight

            print "numLimes:", numLines
            print "charHeight:", charHeight
            # print "extraHeight:", self.extraHeight

            height = numLines * charHeight# + self.extraHeight
            # if numLines > 2:
            #     height += (numLines - 2)*5

            print "height: ", height
            print "size:", self.GetSize()
            # print self.GetMinHeight()

            if height > self.InitHeight:
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
            elif self.GetMinHeight() != self.InitHeight:
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

    def SetFontStyle(self, fontColor = None, fontFace = None, fontSize = None,
                     fontBold = None, fontItalic = None, fontUnderline = None):
        self.textAttr = self.GetDefaultStyle()
        if fontColor:
            self.textAttr.SetTextColour(fontColor)
        if fontFace:
            font = self.textAttr.GetFont()
            font.SetFaceName(fontFace)
            self.textAttr.SetFont(font)
        if fontSize:
            font = self.textAttr.GetFont()
            font.SetPointSize(fontSize)
            self.textAttr.SetFont(font)
        if fontBold != None:
            font = self.textAttr.GetFont()
            if fontBold:
                font.SetWeight(wx.FONTWEIGHT_BOLD)
            else:
                font.SetWeight(wx.FONTWEIGHT_NORMAL)
            self.textAttr.SetFont(font)
        if fontItalic != None:
            font = self.textAttr.GetFont()
            if fontItalic:
                font.SetStyle(wx.FONTSTYLE_ITALIC)
            else:
                font.SetStyle(wx.FONTSTYLE_NORMAL)
            self.textAttr.SetFont(font)
        if fontUnderline != None:
            font = self.textAttr.GetFont()
            if fontUnderline:
                font.SetUnderlined(True)
            else:
                font.SetUnderlined(False)
            self.textAttr.SetFont(font)
        self.SetDefaultStyle(self.textAttr)
        self.SetStyle(0, 1, self.textAttr)

        font = self.textAttr.GetFont()
        dc = wx.MemoryDC()
        dc.SetFont(font)
        self.charHeight = dc.GetCharHeight()
        print self.charHeight


    def SetBackgroundColour(self, colour):
        wx.TextCtrl.SetBackgroundColour(self, colour)

        self.SetDefaultStyle(wx.TextAttr(wx.NullColour, colour));
