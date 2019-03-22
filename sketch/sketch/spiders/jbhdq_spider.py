#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''
scrapy crawl jbhdq --nolog
'''

import scrapy
import ssl  # SSL: CERTIFICATE_VERIFY_FAILED
import re
from scrapy.http import Request
import urllib.request
import socket  # timeout
import os

# Python 升级到 2.7.9 之后引入了一个新特性，当你urllib.urlopen一个 https 的时候，会验证一次 SSL 证书，
# 当目标网站使用的是自签名的证书时就会爆出一个
# urllib2.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:581)>的错误消息
# 解决方法：
ssl._create_default_https_context = ssl._create_unverified_context

# 可能会timeout：
socket.setdefaulttimeout(10)


class jbhdq_spider(scrapy.Spider):
    name = 'jbhdq'
    allowed_domains = ['www.jbhdq.com']
    start_urls = [
        r'https://www.jbhdq.com/jiaotong/index.html',
    ]
    have_read = []
    headers = {
        "HOST": "www.jbhdq.com",
        "Referer": "https://www.jbhdq.com/jiaotong/index.html",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):
        # 分析页面
        # 找到页面中所有的符合的内容（简笔画），并根据内容保存
        # sel = HtmlXPathSelector(response)  # 创建查询对象
        # HtmlXpathSelector 已被弃用，推荐使用Selector
        sel = scrapy.Selector(response=response)
        res = r'https://www.jbhdq.com/[a-z]+/list_[0-9]+.html'
        res2 = r'https://www.jbhdq.com/[a-z]+/index.html'
        img_re = re.compile(r'data-echo="(https://www.jbhdq.com/uploadfile.*\.jpg)')  # 匹配图片
        name_re = re.compile(r'alt="(.*?)"')  # 去贪婪
        print(response.url)  # https://www.jbhdq.com/renwu/index.html
        # 如果url是 https://www.jbhdq.com/[a-z]+/index.html 或 https://www.jbhdq.com/[a-z]+/list_[0-9]+.html
        if re.match(res, response.url) or re.match(res2, response.url):  # 如果url能够匹配到需要爬取的url，即本站url
            items = sel.xpath('//div[@class="wrapper"]/ul[@class="wall"]//li//a//img').extract()
            # print(items)
            for i in items:
                is_ok = False
                print('start')

                print(i)
                # print(items[0])
                # <img src="/statics/images/blank.gif" data-echo="https://www.jbhdq.com/uploadfile/2018/0815/thumb_450_300_20180815011939759.jpg" alt="华贵的古代公主" width="255">
                # 使用正则表达式获取url和名称
                try:
                    src = re.findall(img_re, i)
                    name = re.findall(name_re, i)  # 返回list
                except:
                    src = name = []
                    pass

                print(name, src)
                if len(src) and len(name):
                    abs_src = src[0]
                    print(abs_src)
                    if name[0][-4:] == '的简笔画' and name[0][0] == '画':
                        new_name = name[0][1:-4]
                    elif name[0][-4:] == '的简笔画':
                        new_name = name[0][:-4]
                    elif name[0][-3:] == '简笔画':
                        new_name = name[0][:-3]
                    else:
                        new_name = name[0]
                    file_name = "%s.jpg" % (new_name)
                    download_path = r'/Users/guoxiaojun/Desktop/简笔画/img'
                    try:
                        os.mkdir(download_path)
                    except:
                        pass
                    file_path = os.path.join(download_path, file_name)
                    print(file_path)
                    context = ssl._create_unverified_context()
                    aa = urllib.request.urlopen(abs_src, timeout=5).read()
                    if aa:
                        urllib.request.urlretrieve(abs_src, file_path)

                        # time.sleep(random.randint(10))

        # 获取所有的url，继续访问，并在其中寻找相同的url
        all_a = sel.xpath('//a').extract()
        print('len=%d' % len(all_a))
        # 匹配html
        all_urls = []
        url_re = re.compile(r'.*href="(.*list.*\.html)".*')
        for a in all_a:
            print(a)
            urls = re.findall(url_re, a)
            for url in urls:
                # print(url)
                if ('https://www.jbhdq.com' + url).startswith(response.url[:26]):
                    all_urls.append('https://www.jbhdq.com' + url)

        # response.url
        for url in all_urls:
            print(url)
            if url not in jbhdq_spider.have_read:
                jbhdq_spider.have_read.append(url)
                yield Request(url, callback=self.parse)


                # 总结
                # ^ 匹配字符串的开始。
                # $ 匹配字符串的结尾。
                # \b 匹配一个单词的边界。
                # \d 匹配任意数字。
                # \D 匹配任意非数字字符。
                # x? 匹配一个可选的 x 字符 (换言之，它匹配 1 次或者 0 次 x 字符)。
                # x* 匹配0次或者多次 x 字符。
                # x+ 匹配1次或者多次 x 字符。
                # x{n,m} 匹配 x 字符，至少 n 次，至多 m 次。
                # (a|b|c) 要么匹配 a，要么匹配 b，要么匹配 c。
                # (x) 一般情况下表示一个记忆组 (remembered group)。你可以利用 re.search 函数返回对象的 groups() 函数获取它的值。
                # 正则表达式中的点号通常意味着 “匹配任意单字符”
