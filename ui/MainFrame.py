import logging
import random

import wx
import wx.adv


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, id=wx.NewId(), parent=parent, title=title, size=(800, 600))
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        menuItem = fileMenu.Append(wx.ID_ABOUT, u"关于", u"关于程序的信息")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuItem)
        fileMenu.AppendSeparator()
        menuItem = fileMenu.Append(wx.ID_EXIT, u"退出", u"终止应用程序")
        self.Bind(wx.EVT_MENU, self.OnExit, menuItem)
        menuBar.Append(fileMenu, u"文件")
        self.SetMenuBar(menuBar)
        panel = wx.Panel(self, -1)
        icon_obj = wx.Icon(name="res/drawable/logo.png", type=wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon_obj)  # 设定图标
        self.taskBarIcon = Balloon(self)
        self.button = wx.Button(panel, -1, u"单击我", pos=(50, 20))
        self.CreateStatusBar()  # 创建位于窗口的底部的状态栏
        # 绑定事件，就是指定的button被单击后调用onClick()成员函数
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()
        self.clicked_times = 0
        self.Bind(wx.EVT_CLOSE, self.OnClose)  # 判断窗口关闭

    def OnAbout(self, event):
        print('click about')
        logger = logging.getLogger(__name__)
        logger.info('test')
        dlg = wx.MessageDialog(self, "A small text editor.",
                               "About Sample Editor", wx.OK)  # 语法是(self, 内容, 标题, ID)
        dlg.ShowModal()  # 显示对话框
        dlg.Destroy()  # 当结束之后关闭对话框

    def OnExit(self, event):
        self.Close(True)

    def OnClick(self, event):
        self.clicked_times = self.clicked_times + 1
        # 一旦单击就修改按钮的显示文字
        self.button.SetLabel(u"单击成功(%d)" % self.clicked_times)

    def OnClose(self, event):
        logging.info('OnClose -- to hide')
        self.Hide()
        pass


class Balloon(wx.adv.TaskBarIcon):
    ICON = "res/drawable/logo.png"

    def __init__(self, parent):
        self.mainFrame = parent
        wx.adv.TaskBarIcon.__init__(self)
        self.toolTip = random.randint(0, 1000)
        self.SetIcon(wx.Icon(self.ICON), str(self.toolTip))
        self.Bind(wx.adv.EVT_TASKBAR_MOVE, self.onIconMove)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.onIconClick)

    # Menu数据
    def setMenuItemData(self):
        return ("打开", self.OnMenuClick, wx.ID_OPEN),\
               ("关闭", self.OnMenuClick, wx.ID_CLOSE)

    # 创建菜单
    def CreatePopupMenu(self):
        menu = wx.Menu()
        for itemName, itemHandler, menuId in self.setMenuItemData():
            if not itemName:  # itemName为空就添加分隔符
                menu.AppendSeparator()
                continue
            menuItem = wx.MenuItem(None, menuId, text=itemName, kind=wx.ITEM_NORMAL)  # 创建菜单项
            menu.Append(menuItem)  # 将菜单项添加到菜单
            self.Bind(wx.EVT_MENU, itemHandler, menuItem)
        return menu

    def onIconMove(self, event):
        self.toolTip = random.randint(0, 1000)

    def onIconClick(self, event):
        if self.mainFrame.IsIconized():
            self.mainFrame.Iconize(False)
        if not self.mainFrame.IsShown():
            self.mainFrame.Show(True)
        self.mainFrame.Raise()

    def OnMenuClick(self, event):
        menuId = event.GetId()
        if menuId == wx.ID_OPEN:
            self.onIconClick(event)
        elif menuId == wx.ID_CLOSE:
            wx.Exit()
