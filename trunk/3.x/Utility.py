#!/usr/bin/python
# coding=cp936
# python 3.x

import os
import time
import zipfile
import tempfile

import UserException
import ToolDir


#**************************************
#      For extension
#**************************************
#--------------------------------------
#      File hash
#--------------------------------------
import HashMD5
hash_algorithm = HashMD5.HashMD5()
##import HashModifyTime
##hash_algorithm = HashModifyTime.HashModifyTime()

def get_file_hash(file):
    return hash_algorithm.get_hash(file)



#**************************************
#      Utility functions
#**************************************
#--------------------------------------
#      Modify time
#--------------------------------------

def get_modify_time(file = None):
    '''Time like: 2007-06-02 04:55:02'''
    ISOTIMEFORMAT  ='%Y-%m-%d %X'
    if not file:
        return time.strftime(ISOTIMEFORMAT, time.localtime())  # current time
    return time.strftime(ISOTIMEFORMAT, time.localtime(os.stat(file).st_mtime) )

def modify_time(infolist):
    '''Modify all extract files's modify and access time to their real time'''
    FORMAT = '%Y-%m-%d %H:%M:%S'
    FORMAT_S = '%d-%d-%d %d:%d:%d'
    for zi in infolist:
        time_float = time.mktime(time.strptime(FORMAT_S % zi.date_time, FORMAT) )
        os.utime(zi.filename, (time_float, time_float))
    return

#--------------------------------------
#      Uncompress file
#--------------------------------------
def ziw2html(ziw_file):
    '''Uncompress WizKnowedge file ziw.'''
    temp_path = tempfile.mkdtemp(prefix='pyblogpost_')
    zf = zipfile.ZipFile(ziw_file, 'r' ,zipfile.ZIP_DEFLATED)
    zf.extractall(temp_path)
    os.chdir(temp_path)
    #modify_time(zf.infolist())
    zf.close()
    return 'index.html'

#--------------------------------------
#      print info
#--------------------------------------
def print_t(str):
    print("%s %s" %(time.strftime("%H:%M:%S",time.localtime()), str))


#--------------------------------------
#      File path
#--------------------------------------
def get_file_suffix(file):
    '''Get file extension name.

    If file= abc.jpg, then return jpg'''
    return file[file.rindex('.') + 1:]


#--------------------------------------
#      Try execute
#--------------------------------------
def try_exec(exception, times, delay, func, *params):
    '''
    try exec func for at most 'times' times.

    if func() raise exception, then delay for 'delay' seconds and to try again, until times.
    func must use a tuple param.

    params is always a tuple.

    XXX: how to support multi exceptions?
    '''
    for i in range(times):  # i is from 0 to times-1
        try:
            if i >= 1:
                print_t('Delay %d seconds to retry the %d time...' % (delay, i + 1))
                time.sleep(delay)  # sleep delay seconds
            return func(params)
        except exception as ex:  # ex is a instance of exception
            print_t(ex)
            continue
    raise UserException.TryTimeOutException

def save_file(file, string):
    f = open(file, 'w')
    f.write(string)
    f.close()

def tool_dir(need_sep):
    if need_sep:
        return ToolDir.get_main_dir() + os.path.sep
    return ToolDir.get_main_dir()

# print debug info.
# use: u.debug.print("some info")
class debug:
    is_debug = False
    def print(string):
        if debug.is_debug:
            print_t(string)


#module test
##print(get_file_hash('blogdata.xml'))
##print(get_file_ext('blogdata.xml'))


## can not support this
##def test_try_exec2(str, str2):
##    print(str)
##    print(str2)
##    raise UserException.NotFoundException
##    return

##def test_try_exec(str):
##    print(str)
##    raise UserException.NotFoundException
##    return
##try_exec(UserException.NotFoundException, 3, 2, test_try_exec, 'str for test', 'str for test')
