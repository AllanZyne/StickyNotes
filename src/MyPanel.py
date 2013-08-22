# -*- coding:utf-8 -*-
import wx

class MyPanel(wx.Panel):
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent, size = size)


        self.MakeContextMenu()

        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)


    def MakeContextMenu(self):
        menu_titles = [ u"置顶",
                        u"锁定位置",
                        u"锁定编辑",
                        u"关闭(&C)\tAlt+F4" ]
        menu_id = []
        for title in menu_titles:
            menu_id.append(wx.NewId())

        self.Bind(wx.EVT_MENU, self.OnPinned, id=menu_id[0])
        self.Bind(wx.EVT_MENU, self.OnLockPos, id=menu_id[1])
        self.Bind(wx.EVT_MENU, self.OnLockEdit, id=menu_id[2])
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_CLOSE)

        self.menu = menu = wx.Menu()

        menu.AppendCheckItem(menu_id[0], menu_titles[0]).Check(True)
        menu.AppendCheckItem(menu_id[1], menu_titles[1])
        menu.AppendCheckItem(menu_id[2], menu_titles[2])
        menu.AppendSeparator()
        menu.Append(wx.ID_CLOSE, menu_titles[3])


    def OnContextMenu(self, evt):
        self.PopupMenu(self.menu)


    def OnPinned(self, evt):
        if evt.IsChecked():
            self.GetParent().Pinned(True)
        else:
            self.GetParent().Pinned(False)


    def OnLockPos(self, evt):
        if evt.IsChecked():
            self.GetParent().LockPos(True)
        else:
            self.GetParent().LockPos(False)

    def OnLockEdit(self, evt):
        if evt.IsChecked():
            self.GetParent().LockEdit(True)
        else:
            self.GetParent().LockEdit(False)

    def OnExit(self, evt):
        self.menu.Destroy()
        self.GetParent().Exit()