#!/usr/bin/python
# coding=cp936
# python 3.x

import lxml.etree
import XmlProc
import UserException


class BlogData:
    def __init__(self, file = None, string = None):
        if file :
            self.file = file
            try:
                self.tree = lxml.etree.parse(file)
            except:
                self.tree = lxml.etree.fromstring('<data/>')  # if read file fail, create root data.
        elif string :
            self.tree = lxml.etree.fromstring(string)
        else :
            raise UserException.ParamException


    def get_media_list(self, guid):
        '''
        Get media file(s).

        Returns:
        at least [{'local_path':'file_hash'}, {'local_path2':'file_hash2'}]
        real return is much more
        '''
        temp_string = lxml.etree.tostring(self.tree)
        xml = XmlProc.XmlProc(in_string = temp_string)
        return xml.get_dict_of_dict("/data/html_file[@wk_file_guid='"+guid+"']/media/file", 'local_path')

    def update_media_files(self, guid, media_files):
        '''
        Update media file(s).

        Args:
        draft: media_files = {'local_path':['remote_path', 'file_hash', 'isAdd'], 'local_path2':['remote_path2', 'file_hash2', 'isAdd2']}
        draft: isAdd is a bool value, True for add, False for update.
        '''
        html_node = self.get_html_node(guid)
        media_node = self.get_media_node(html_node)
        #remove all old content in media_node
        media_node.clear()
        temp_string = lxml.etree.tostring(self.tree)
        xml = XmlProc.XmlProc(in_string = temp_string)
        xml.add_children("/data/html_file[@wk_file_guid='"+guid+"']/media", 'file', media_files, 'local_path')
        self.tree = xml.tree
        pass

    def get_only_node(self, xpath):
        nodes = self.tree.xpath(xpath)
        if not nodes:
            raise UserException.NotFoundException
        elif len(nodes) > 1:
            raise UserException.TooManyNodesException
        return nodes[0]

    def update_node_text(self, parent_xpath, tag, text):
        '''If not exist, create.'''

        try:
            nodes = self.tree.xpath(parent_xpath + '/' + tag)
        except:
            pass

        if not nodes: # not found
            temp = lxml.etree.Element(tag)
            temp.text = text
            parent = self.get_only_node(parent_xpath)
            parent.append(temp)
            return

        # found
        for node in nodes:
            node.text = text

    def update_media(self, guid, local_path, remote_path, file_hash):
        '''
        Update media file info.

        Args:
        '''
        html_node = self.get_html_node(guid)
        media_node = self.get_media_node(html_node)
        file_nodes = media_node.xpath("/data/html_file[@wk_file_guid='"+guid+"']/media/file[@local_path='"+local_path+"']")
        if not file_nodes : # not found that node
            file_node = lxml.etree.Element('file')
            file_node.set('local_path', local_path)
            media_node.append(file_node)

        self.update_node_text("/data/html_file[@wk_file_guid='"+guid+"']/media/file[@local_path='"+local_path+"']", 'remote_path', remote_path)
        self.update_node_text("/data/html_file[@wk_file_guid='"+guid+"']/media/file[@local_path='"+local_path+"']", 'file_hash', file_hash)
        #how to get child with sepcified tag?
        return

    def get_blogs(self, guid) :
        temp_string = lxml.etree.tostring(self.tree)
        xml = XmlProc.XmlProc(in_string = temp_string)
        return xml.get_dict_of_dict("/data/html_file[@wk_file_guid='"+guid+"']/blog", 'name')

    def add_blog(self, guid, blog_name, postid, file_hash):
        '''
        Add blog record.

        Args:
        '''
        html_node = self.get_html_node(guid)
        blog_node = lxml.etree.Element('blog')
        blog_node.set('name', blog_name)
        temp_node = lxml.etree.Element('postid')
        temp_node.text = str(postid)
        blog_node.append(temp_node)
        temp_node = lxml.etree.Element('file_hash')
        temp_node.text = file_hash
        blog_node.append(temp_node)
        html_node.append(blog_node)
        pass

    def update_blog(self, guid, blog_name, file_hash):
        '''
        Update blog record.

        Args:
        '''
        html_node = self.get_html_node(guid)
        blog_nodes = html_node.xpath("blog[@name='"+blog_name+"']")  #/data/html_file[@wk_file_guid=]/
        blog_node = blog_nodes[0]
        file_hash_nodes = blog_node.xpath('file_hash')
        file_hash_node = file_hash_nodes[0]
        file_hash_node.text = file_hash

    def get_html_node(self, guid):
        html_nodes = self.tree.xpath("//html_file[@wk_file_guid='"+guid+"']")
        if not html_nodes :
            html_node = lxml.etree.Element('html_file')
            html_node.set('wk_file_guid', guid)
            root = self.tree.xpath("/data")[0]
            root.append(html_node)
        else :
            if len(html_nodes) > 1:
                raise UserException.TooManyNodesException
            html_node = html_nodes[0]
        return html_node


    def get_media_node(self, html_node):
        media_nodes = html_node.xpath("media")
        if not media_nodes :
            media_node = lxml.etree.Element('media')
            html_node.append(media_node)
        else :
            if len(media_nodes) > 1:
                raise UserException.TooManyNodesException
            media_node = media_nodes[0]
        return media_node

    def write_file(self):
        '''
        Write xml data to file.

        '''
        file = open(self.file, 'w')
        file.write(lxml.etree.tostring(self.tree).decode())
        file.close()


#module test
##data = BlogData('justtest.xml')
##data.write_file()

##father = lxml.etree.fromstring('<father/>')
##me = lxml.etree.Element('me')
##father.append(me)
##brother = lxml.etree.Element('brother')
##father.append(brother)
##son = lxml.etree.Element('son')
##me.append(son)
##son2 = lxml.etree.Element('son')
##brother.append(son2)
##print(lxml.etree.tostring(father))
##print(lxml.etree.tostring(me))
##print(son)
##print(son2)
##nodes = me.xpath('/father/me/son')
##print(nodes)
##nodes = me.xpath('/me/son')
##print(nodes)
##nodes = me.xpath('son')
##print(nodes)
##nodes = me.xpath('/son')
##print(nodes)
##nodes = me.xpath('/')
##print(nodes)
##nodes = me.xpath('//son')
##print(nodes)
###nodes = me.xpath('') exception


