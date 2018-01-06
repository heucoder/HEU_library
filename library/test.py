#coding:utf-8
from librarymodel import modellib

m = modellib()
m.login('2014022125', 'yt121116')

# m.context()
# m.continue_lend()
# m.personinfo()
# m.getname()
name = u'c++'
page = 1
m.search(name, page)
# m.bookhist()