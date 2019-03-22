#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import os
import urllib.request
def main():
    print(len('https://www.jbhdq.com/renwu/'))
    # abs_src =r'https://www.jbhdq.com/uploadfile/2018/0906/thumb_450_300_20180906102334382.jpg'
    # file_path = r'/Users/guoxiaojun/Desktop/简笔画/img/漂亮的姐姐.jpg'
    # urllib.request.urlretrieve(abs_src, file_path)
    # download_path = r'/Users/guoxiaojun/Desktop/简笔画/img'
    # try:
    #     os.mkdir(download_path)
    # except:
    #     pass

    name = '六一节可爱的小女孩简笔画'
    print(name[:-3])

    s = 'https://www.jbhdq.com/renwu/list_2.html'
    s = 'https://www.jbhdq.com/renwu/index.html'

    res = r'https://www.jbhdq.com/[a-z]+/list_[0-9]+.html'
    res2 = r'https://www.jbhdq.com/[a-z]+/index.html'
    res3 = r'https://www.jbhdq.com/[a-z]+/'
    find = re.match(res3, s).group()
    print(find)
    try:
        find = re.match(res,s).group()
        print(find)
    except AttributeError:
        print('error')
        try:
            find = re.match(res2, s).group()
            print(find)
        except AttributeError:
            print('error2')

    if re.match(res2, s):
        print(1)

    a = []
    if not a:
        print('empty')



def png():
    img_re = re.compile(
        r'data-echo="(https://www.jbhdq.com/uploadfile.*\.jpg)')  # 匹配图片
    string = '<img src="/statics/images/blank.gif" data-echo="https://www.jbhdq.com/uploadfile/2018/0720/thumb_450_300_20180720015757101.jpg" alt="背书包的小女孩" width="255">'
    src = re.findall(img_re, string)
    print(src)



if __name__=='__main__':
    png()