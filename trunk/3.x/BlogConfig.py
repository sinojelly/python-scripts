#!/usr/bin/python
# coding=cp936
# python 3.x

import lxml.etree
import XmlProc
import UserException


class BlogConfig:
    def __init__(self, file = None, string = None):
        if file :
            xml = XmlProc.XmlProc(in_file = file)
        elif string :
            xml = XmlProc.XmlProc(in_string = string)
        else :
            raise UserException.ParamException

        self.fileserver = xml.get_list_of_dict('/config/fileserver')
        self.blogs = xml.get_list_of_dict('/config/blog')

    def get_fileserver(self) :
        """
        Get fileserver parameters.

        Returns:
            List of fileserver parameters(posturl/username/password) dictionary.
        """
        return self.fileserver

    def get_blogs(self):
        """
        Get blogs parameters.

        list_blog[0] = [{'name':'servername', 'system':'wordpress', 'posturl':url, 'username':usr, 'password':pass, 'upload':'false'}]
        Returns:
            List of blogs parameters(system/posturl/username/password/upload) dictionary.
        """
        return self.blogs


##raise UserException.ParamException
##BlogConfig()
