#coding:utf-8
import wx
import threading
from librarymodel import modellib

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(parent=None, id=-1, title='HEU_libraray')
        frame.Show(True)
        return True

class SearchThread(threading.Thread):
    def __init__(self, window, name, page, m):
        threading.Thread.__init__(self)
        self.window = window
        self.page = page
        self.name = name
        self.m = m

    def stop(self):
        pass

    def run(self):
        info = self.m.search(self.name, self.page)
        wx.CallAfter(self.window.adddata, info)


class WorkerThread(threading.Thread):
    def __init__(self, window, n, m):
        threading.Thread.__init__(self)
        self.window = window
        self.n = n
        self.m = m

    def stop(self):
        pass

    def run(self):

        if self.n == 1:
            #当前借阅
            info = self.m.booklist()
            wx.CallAfter(self.window.adddata, info)
        elif self.n == 2:
            #个人信息
            info = self.m.personinfo()
            wx.CallAfter(self.window.adddata, info)
        elif self.n == 3:
            #一键借书
            self.m.continue_lend()
            pass
        elif self.n == 4:
            #历史借阅
            pass
        elif self.n == 0:
            #登录成功
            info = self.m.getname()
            wx.CallAfter(self.window.setname, info)
            pass

        pass

class MyFrame(wx.Frame):
    def __init__(self,parent, id, title):
        wx.Frame.__init__(self, None, title = title, size=(724, 376))
        panel = wx.Panel(self)

        #控制界面
        self.n = 0
        #当前页数
        self.page = 0
        self.allpage = 0
        self.name = u''

        searchBtn = wx.Button(panel, -1, "搜索")
        preBtn = wx.Button(panel, -1, "上一页")
        nextBtn = wx.Button(panel, -1, "下一页")
        bookhistBtn = wx.Button(panel, -1, "借阅历史")
        booklistBtn = wx.Button(panel, -1, "当前借阅")
        lendBtn = wx.Button(panel, -1, "一键还书")
        personInfoBtn = wx.Button(panel, -1, "个人信息")
        loginBtn = wx.Button(panel, -1, "登录")
        self.tc_search = wx.StaticText(panel, -1, "题名-前方一致:")
        self.tc_page = wx.StaticText(panel, -1, "0/00")
        self.search = wx.TextCtrl(panel, -1, "",size=(280,25))
        self.tc = wx.StaticText(panel, -1, "姓名: 00")
        self.tc_account = wx.StaticText(panel, -1, "账号:")
        self.account = wx.TextCtrl(panel, -1, "",)
        self.tc_password = wx.StaticText(panel, -1, "密码:")
        self.password = wx.TextCtrl(panel, -1, "",style=wx.TE_PASSWORD)
        self.log = wx.TextCtrl(panel, -1, "",style=wx.TE_RICH | wx.TE_MULTILINE)
        self.m = modellib()

        inner_up = wx.BoxSizer(wx.VERTICAL)
        inner_up.Add(bookhistBtn, 0, wx.LEFT | wx.TOP, 5)
        inner_up.Add((-1, 10))
        inner_up.Add(booklistBtn, 0, wx.LEFT, 5)
        inner_up.Add((-1, 10))
        inner_up.Add(lendBtn, 0, wx.LEFT, 5)
        inner_up.Add((-1, 10))
        inner_up.Add(personInfoBtn, 0, wx.LEFT, 5)
        inner_up.Add((-1, 10))

        inner_bottom = wx.BoxSizer(wx.VERTICAL)
        inner_bottom.Add(self.tc_account, 0, wx.LEFT,5)
        inner_bottom.Add(self.account, 0, wx.LEFT, 5)
        inner_bottom.Add(self.tc_password, 0, wx.LEFT, 5)
        inner_bottom.Add(self.password, 0, wx.LEFT, 5)
        inner_bottom.Add((-1, 10))
        inner_bottom.Add(loginBtn, 0, wx.LEFT, 5)
        inner_bottom.Add((-1, 15))
        inner_bottom.Add(self.tc, 0, wx.CENTER, 5)

        inner = wx.BoxSizer(wx.VERTICAL)
        inner.Add(inner_up, 0, wx.ALIGN_TOP, 10)
        inner.Add(inner_bottom, 0, wx.ALIGN_BOTTOM, 10)

        right_bottom_inner = wx.BoxSizer(wx.HORIZONTAL)
        right_bottom_inner.Add(self.tc_search, 0, wx.ALIGN_CENTER_VERTICAL,)
        right_bottom_inner.Add(self.search, 1, wx.EXPAND | wx.ALL, 5)
        right_bottom_inner.Add(self.tc_page, 0, wx.ALIGN_CENTER_VERTICAL,)
        right_bottom_inner.Add(searchBtn, 0, wx.EXPAND, 5)
        right_bottom_inner.Add(preBtn, 0, wx.EXPAND, 5)
        right_bottom_inner.Add(nextBtn, 0, wx.EXPAND, 5)

        right_inner = wx.BoxSizer(wx.VERTICAL)
        right_inner.Add(self.log, 1, wx.EXPAND | wx.ALL, 5)
        right_inner.Add(right_bottom_inner, 0, wx.ALIGN_BOTTOM, 10)

        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(inner, 0, wx.ALIGN_LEFT, 10)
        main.Add(right_inner, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(main)
        self.Bind(wx.EVT_BUTTON, self.OnLoginButton, loginBtn)
        self.Bind(wx.EVT_BUTTON, self.OnPersonInfoButton, personInfoBtn)
        self.Bind(wx.EVT_BUTTON, self.OnLendButton, lendBtn)
        self.Bind(wx.EVT_BUTTON, self.OnBookListButton, booklistBtn)
        self.Bind(wx.EVT_BUTTON, self.OnSearchButton, searchBtn)
        self.Bind(wx.EVT_BUTTON, self.OnSearchButton, preBtn)
        self.Bind(wx.EVT_BUTTON, self.OnSearchButton, nextBtn)

        #这个暂时未完成
        self.Bind(wx.EVT_BUTTON, self.OnBookHistButton, bookhistBtn)

    def OnLoginButton(self, evt):
        account = self.account.GetValue()
        password = self.password.GetValue()
        n = self.m.login(account, password)
        if n == 0:
            print u'登录成功'
            self.n = 0
            t = WorkerThread(self, self.n, self.m)
            t.start()
        else:
            print u'登录失败'
            wx.MessageBox(u"账号或密码错误", u"Message", wx.OK | wx.ICON_INFORMATION)
        pass

    def OnPersonInfoButton(self, evt):
        self.n = 2
        t = WorkerThread(self, self.n, self.m)
        t.start()

    def OnLendButton(self, evt):
        self.n = 3
        t = WorkerThread(self, self.n, self.m)
        t.start()
        wx.MessageBox(u"续借成功", u"HEU_library", wx.OK | wx.ICON_INFORMATION)
        pass

    def OnBookListButton(self, evt):
        self.n = 1
        t = WorkerThread(self, self.n, self.m)
        t.start()

    def OnBookHistButton(self, evt):
        self.n = 4

        pass

    #开新线程
    def OnSearchButton(self, evt):
        eventbutton = evt.GetEventObject()
        label = eventbutton.GetLabel()
        if label == u'搜索':
            self.page = 1
        elif label == u'上一页':
            self.page -= 1
        elif label == u'下一页':
            self.page += 1
        self.name = self.search.GetValue()
        info = self.m.search(self.name, self.page)
        self.allpage = info[0]
        label = str(self.page) + u'/'+ self.allpage
        self.tc_page.SetLabel(label)
        self.adddata(info[1:])
        #不能用线程，py2.7有点尴尬
        # t = SearchThread(self, self.name, self.page, self.m)
        # t.start()
        #

    def adddata(self, infolist):
        info = u''
        for item in infolist:
            info += item +u'\t\n'
        self.log.Clear()
        self.log.SetValue(info)

    def setname(self, infolist):
        self.tc.SetLabel(u"姓名: %s" % infolist)

def main():
    app = MyApp()
    app.MainLoop()

if __name__ == '__main__':
    main()
