#coding:utf-8

import os.path
from PIL import Image

#获得验证码的类，对外部不可见
class captcha_ver:
    def __init__(self, threshold = 140):
        self.threshold = threshold

    def __get_bin_table(self):
        """
        获取灰度转二值的映射table
        :param threshold:
        :return:
        """
        table = []
        for i in range(256):
            if i < self.threshold:
                table.append(0)
            else:
                table.append(1)

        return table

    def __get_in(self, img_path):
        image = Image.open(img_path)
        imgry = image.convert('L')  # 转化为灰度图

        table = self.__get_bin_table()
        out = imgry.point(table, '1')
        box1 = (6, 16, 14, 26)
        box2 = (18, 16, 26, 26)
        box3 = (30, 16, 38, 26)
        box4 = (42, 16, 50, 26)
        listbox = [box1, box2, box3, box4]
        listdata = []
        for item in listbox:
            listdata.append(out.crop(item))
        return listdata

    def __get_standard(self):
        listnum = []
        for i in range(10):
            path = 'process_data/num' + str(i) + '.bmp'
            im = Image.open(path)
            img1 = im.convert('L')  # 转化为灰度图

            table = self.__get_bin_table()
            tout = img1.point(table, '1')
            listnum.append(tout)
        return listnum

    def __get_error(self, im1, im2):
        sum = 0
        for i in range(8):
            for j in range(10):
                if (im1.getpixel((i, j)) != im2.getpixel((i, j))):
                    sum += 1
        return sum

    def get_num_captcha(self, img_path):
        res = ""
        listdata = self.__get_in(img_path)
        listnum = self.__get_standard()
        for item1 in listdata:
            error = 90
            num = 0
            for i in range(len(listnum)):
                item2 = listnum[i]
                gerror = self.__get_error(item1, item2)
                if (gerror < error):
                    error = gerror
                    num = i
            res += str(num)
        return res

    def searchbook(self, name, page):
        index_url = 'http://202.118.176.18:8080/opac/openlink.php?location=ALL&title=c%2B%2B&doctype=ALL&lang_code=ALL&match_flag=forward&displaypg=20&showmode=list&orderby=DESC&sort=CATA_DATE&onlylendable=no&count=808&with_ebook=on&page=1'
