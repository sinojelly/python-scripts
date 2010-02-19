#!/usr/bin/python
# coding=cp936
# python 3.x

import re

import Utility as u

class HtmlProc:
    def __init__(self, file):
        self.media_files = []
        self.media_times = {}
        self.init_html_content(file)
        self.init_media_files()
        self.html_time = u.get_modify_time(file)

    def get_html_title(self):
        return self.html_title

    def get_html_body(self):
        '''Get html body without media path replaced.'''
        return self.html_body

    def get_html_time(self):
        return self.html_time

    def get_media_time(self, media):
        return self.media_times[media]

    def get_media_files(self):
        return self.media_files

    def update_html_body(self, html_body, media, url):
        p = re.compile(media,re.S|re.I)
        return p.sub(url, html_body)  #替换html文件中的img图片路径为网络路径

    def init_media_files(self):
        '''Get list of media files path.'''

    	#大小写忽略，也可以用re.I
        u.print_t("Get media list...")
        p = re.compile(r'''.*?<.*?IMG.*?src\s*=\s*"(.*?)".*?>.*?''',re.S|re.I)   #必须有前后的.*

        iterator = p.finditer(self.html_body)
        for match in iterator:
            media = match.group(1)
            self.media_files.append(media)
            self.media_times[media] = u.get_modify_time(media)

    def init_html_content(self, filename):
        u.print_t("Parsing "+filename+" content...")
        #打开带图的html文件(Unicode编码)
        html_file = open(filename, encoding='utf-16')
        html_content = html_file.read()
        html_file.close()

        #删除\r\n和\n, re.S表示.能匹配\n
        p = re.compile(r"\r?\n",re.S)
        html_content = p.sub("",html_content)

    	#去掉头
        p = re.compile(r'<!DOCTYPE HTML PUBLIC.*<TITLE>(.*)</TITLE>.*<BODY>',re.S)
        self.html_title = p.match(html_content).group(1)
        self.html_body = p.sub("",html_content)

    	#去掉尾
        p = re.compile(r'</BODY>.*</HTML>',re.S)
        self.html_body = p.sub("",self.html_body)

