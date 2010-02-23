#!/usr/bin/python
# coding=cp936
# python 3.x

import hashlib


class HashMD5:
    def get_hash(self, file):
        ##f = open(file, 'r', encoding = 'UTF-8')
        f = open(file, 'rb')  # Jelly: use 'rb' to avoid encoding problem, and the MD5 is the same.
        m = hashlib.md5()
        ##m.update(f.read().encode())
        m.update(f.read())
        f.close()
        return m.hexdigest()
    pass


#module test
##h = HashMD5()
##print(h.get_hash('blogdata.xml'))

###XXX: not ok, chardet not exist
##import urllib
##urlread = lambda url: urllib.urlopen(url).read()
##import chardet
##chardet.detect(urlread("http://google.cn/"))