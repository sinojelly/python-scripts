#!/usr/bin/python
# coding=cp936
# python 3.x

import XmlProc

class MIME:
    def __init__(self, file):
        tree = XmlProc.XmlProc(file)
        self.table = tree.get_dict_of_dict('/config/mime', 'suffix')
    def get_mime_type(self, suffix):
        return self.table[suffix]['mime_type']
    pass

#module test
##m = MIME('MIME.xml')
##print(m.get_mime_type('jpg'))

