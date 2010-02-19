#!/usr/bin/python
# coding=cp936
# python 3.x

import Utility as u


class HashModifyTime:
    def get_hash(self, file):
        return u.get_modify_time(file)
    pass


#module test
##h = HashMD5()
##print(h.get_hash('blogdata.xml'))
