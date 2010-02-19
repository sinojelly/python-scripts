#!/usr/bin/python
# coding=cp936
# python 3.x

import os
import time
import zipfile
import tempfile

def get_modify_time(file):
    '''Time like: 2007-06-02 04:55:02'''
    ISOTIMEFORMAT  ='%Y-%m-%d %X'
    return time.strftime(ISOTIMEFORMAT, time.localtime(os.stat(file).st_mtime) )

def print_t(str):
    print("%s %s" %(time.strftime("%H:%M:%S",time.localtime()), str))


def modify_time(infolist):
    '''Modify all extract files's modify and access time to their real time'''
    FORMAT = '%Y-%m-%d %H:%M:%S'
    FORMAT_S = '%d-%d-%d %d:%d:%d'
    for zi in infolist:
        time_float = time.mktime(time.strptime(FORMAT_S % zi.date_time, FORMAT) )
        os.utime(zi.filename, (time_float, time_float))
    return

def ziw2html(ziw_file):
    '''Uncompress WizKnowedge file ziw.'''
    temp_path = tempfile.mkdtemp(prefix='pyblogpost_')
    zf = zipfile.ZipFile(ziw_file, 'r' ,zipfile.ZIP_DEFLATED)
    zf.extractall(temp_path)
    os.chdir(temp_path)
    modify_time(zf.infolist())
    zf.close()
    return 'index.html'

