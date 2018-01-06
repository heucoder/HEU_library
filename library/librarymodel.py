#coding:utf-8
import requests
import cookielib
import re
from bs4 import BeautifulSoup
import time
from captcha import captcha_ver

#从图书馆主页获得想要的内容
class modellib:
    def __init__(self):
        self.captcha = captcha_ver(140)
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
        Referer = 'http://202.118.176.18:8080/reader/redr_verify.php'
        Host = '202.118.176.18:8080'
        self.headers = {'User-Agent': user_agent,
                   'Referer': Referer,
                   'Host': Host}
        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar(filename='library_cookie')
        pass

    #解决验证码问题，还好图书馆的验证码比较简单
    def __get_captcha(self):
        captcha_url = 'http://202.118.176.18:8080/reader/captcha.php'
        print
        captcha_url
        r = self.session.get(captcha_url)
        with open('captcha.bmp', 'wb') as f:
            f.write(r.content)
            f.close()
        captcha = self.captcha.get_num_captcha('captcha.bmp')
        return captcha

    def __load_cookie(self):
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print('cookie 不成功')

    #通过python模拟续借时间
    def __get_time(self):
        s = "%.3f" % time.time()
        s = s.replace('.', '')
        return s

    #通过正则表达式获得续借的网址
    def __get_code_check(self, html):
        s = re.findall('\'\d*\',\'\w*\',\'\d*\'', html)
        return s

    #登录(后续可能要修改)
    def login(self, account, password):
        login_url = 'http://202.118.176.18:8080/reader/redr_verify.php'
        postdata = {'number': account,
                    'passwd': password,
                    'captcha': self.__get_captcha(),
                    'select': 'cert_no',
                    'returnUrl': ''}
        print self.session.cookies
        login_page = self.session.post(login_url, data=postdata, headers=self.headers)
        if(login_page.url != 'http://202.118.176.18:8080/reader/redr_info.php'):
            print u'账号或者密码错误'
            return -1
            pass
        print login_page.status_code
        self.session.cookies.save()
        return 0

    #获得当前页面内容
    def __gethtml(self, index_url):
        self.__load_cookie()
        res = self.session.get(index_url, headers=self.headers, timeout = 10)
        print res.status_code
        if (res.status_code == 200):
            res.encoding = res.apparent_encoding
            return res.text
        else:
            return None

    def getname(self):
        index_url1 = 'http://202.118.176.18:8080/reader/redr_info.php'
        html = self.__gethtml(index_url1)
        if html != None:
            soup = BeautifulSoup(html, 'html.parser')
            name = soup.find('span', attrs={'class':'profile-name'}).string
            print name
            return name

            pass

    #获得当前借阅的信息
    def booklist(self):
        index_url1 = 'http://202.118.176.18:8080/reader/book_lst.php'
        html = self.__gethtml(index_url1)
        #网络稳定
        if html != None:
            soup = BeautifulSoup(html, 'html.parser')
            # print soup.prettify()
            fr = open('libray.txt', 'wb')
            fr.write(soup.prettify().encode('utf-8'))
            tbody = soup.find_all(name='tr')
            # print tbody
            print len(tbody) - 3
            list = []
            for item in tbody:
                td = item.find_all('td')
                s = ''
                for it in td:
                    s += it.get_text().strip() + ','
                print s + '\n'
                list.append(s)
            #返回当前借阅信息的列表
            return list

    #续借所有
    def continue_lend(self):
        index_url1 = 'http://202.118.176.18:8080/reader/book_lst.php'
        html = self.__gethtml(index_url1)
        if html != None:
            captcha = str(self.__get_captcha())  # 验证码
            soup = BeautifulSoup(html, 'html.parser')
            tbody = soup.find_all(name='tr')
            code_check_list = self.__get_code_check(html)
            for item in code_check_list:
                ls = item.split(',')
                check = ls[1][1:-1]
                bar_code = ls[0][1:-1]
                lendtime = self.__get_time()  # 借阅时间
                lend_url = 'http://202.118.176.18:8080/reader/ajax_renew.php?bar_code=' + bar_code + \
                           '&check=' + check + '&captcha=' + captcha + '&time=' + lendtime
                print lend_url
                res = self.session.get(lend_url)
                print res.text

    def personinfo(self):
        index_url1 = 'http://202.118.176.18:8080/reader/redr_info_rule.php'
        html = self.__gethtml(index_url1)
        if html != None:
            soup = BeautifulSoup(html, 'html.parser')
            tbody = soup.find('body').find('div', attrs = {'id':'mylib_info'})
            tr_list = tbody.find_all('tr')
            infolist = []
            for tr in tr_list:
                td_list = tr.find_all('td')
                s = u''
                for td in td_list:
                    for ss in td.strings:
                        s += ss.strip()
                print s + u'\n'
                infolist.append(s)
            return infolist

    def search(self, name, page):
        index_url1 = 'http://202.118.176.18:8080/opac/openlink.php?location=ALL&title='+name+'&doctype=ALL&lang_code=ALL&match_flag=forward&displaypg=20&showmode=list&orderby=DESC&sort=CATA_DATE&onlylendable=no&count=808&with_ebook=on&page='+str(page)
        url = 'http://202.118.176.18:8080/opac/openlink.php?location=ALL&title=c%2B%2B&doctype=ALL&lang_code=ALL&match_flag=forward&displaypg=20&showmode=list&orderby=DESC&sort=CATA_DATE&onlylendable=no&count=808&with_ebook=on&page=2'
        html = self.__gethtml(index_url1)
        if html:
            res_list = []
            soup = BeautifulSoup(html, 'html.parser')
            span = soup.find('span', attrs={'class':'num_prev'})
            allpage = span.find('b').find_all('font')[1].string
            print allpage
            res_list.append(allpage)
            ol = soup.find('ol', attrs={'id':'search_book_list'})
            li_list = ol.find_all('li')
            for li in li_list:
                s = u''
                s += li.find('h3').text + '\t'
                for ss in li.find('p').strings:
                    s += ss.strip()
                print s
                res_list.append(s)
            return res_list

    def bookhist(self):
        url = 'http://202.118.176.18:8080/reader/book_hist.php'
        postdatas = {'para_string':'all'}
        self.__load_cookie()
        res = self.session.post(url,data=postdatas, headers=self.headers, timeout=10)
        print res.text
        #未完成