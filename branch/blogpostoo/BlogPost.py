
import xmlrpc.client
import sys
import os
##import time

import pyblog

import HtmlProc
import BlogConfig
import BlogData
import Utility as u


class BlogDataX(BlogData.BlogData):
    '''encapsulation complex data structure'''
    def __init__(self, guid, data_file):
        BlogData.BlogData.__init__(self, data_file)
        self.medias = BlogData.BlogData.get_media_list(self, guid)
        self.blogs = BlogData.BlogData.get_blogs(self, guid)

    def get_blog_time(self, blog_name):
        try:
            blog = self.blogs[blog_name]   #if dict has no key names blog_name, it is None? no, it's KeyErr exception
        except:
            return None
        return blog['modify_time']

    def get_media_time(self, media_name):
        try:
            media = self.medias[media_name]
        except:
            return None
        if media:
            return media['modify_time']
    def get_postid(self, blog_name):
        try:
            blog = self.blogs[blog_name]   #if dict has no key names blog_name, it is None? no, it's KeyErr exception
        except:
            return None
        return blog['postid']
    pass

class WordPressX(pyblog.WordPress):
    def __init__(self, posturl, username, password):
        pyblog.WordPress.__init__(self, posturl, username, password)

    def new_post(self, title, body):
        return pyblog.WordPress.new_post(self, self.get_content(title, body))

    def update_post(self, postid, title, body):
        pyblog.WordPress.edit_post(self, postid, self.get_content(title, body))

    def upload_media(self, media):
        file = open(media, "rb")
        content = xmlrpc.client.Binary(file.read())  #base 64 encoding binary
        file.close()
        type = 'image/jpeg'
        if media[-3:] == 'png':
            type = 'image/png'
        elif media[-3:] == 'gif':
            type = 'image/gif'
        media_obj = {'name':media, 'type':type, 'bits':content}
        return pyblog.WordPress.new_media_object(self, media_obj)

    def get_content(self, title, body):
        content = {"description":body, "title":title}
        return content
    pass

class MetaWeblogX(pyblog.MetaWeblog):
    pass

class BlogPost:
    server_class = {}
    server_class = {
        'wordpress':WordPressX,
        'mediaweblog':MetaWeblogX,
    }
    def __init__(self, html_file, html_file_guid, config_file, data_file):
        self.html_proc = HtmlProc.HtmlProc(html_file)
        self.file_name = html_file
        self.file_guid = html_file_guid
        self.config = BlogConfig.BlogConfig(config_file)
        self.data = BlogDataX(html_file_guid, data_file)
        self.new_medias = self.html_proc.get_media_files()
        self.html_title = self.html_proc.get_html_title()
        self.html_body  = self.html_proc.get_html_body()
        fileserver = self.config.get_fileserver()
        blogs = self.config.get_blogs()
        self.servers = [fileserver[0]]
        for blog in blogs :
            self.servers.append(blog)
        pass

    def should_post_media(self, file):
        '''Wither the blog should to post/update this article/media.

        If article not modified, but media modified, the media should post.
        Returns:
        0 --  not post
        1 --  new post
        '''
        new_time = self.html_proc.get_media_time(file)
        old_time = self.data.get_media_time(file)  #time compare
        if not old_time :  # have not post, it's None
            return '1'
        if new_time > old_time :
            return '1'
        return '0'

    def should_post_blog(self, blog_name):
        '''Wither the blog should to post/update this article/media.

        If article not modified, but media modified, the media should post.
        Returns:
        0 --  not post
        1 --  new post
        2 --  update post
        '''
        new_time = self.html_proc.get_html_time()
        old_time = self.data.get_blog_time(blog_name)  #time compare
        if not old_time :  # have not post, it's None
            return '1'
        if new_time > old_time :
            return '2'
        return '0'

    def new_blog(self, blog, server):
        html_body = self.post_medias(blog, server)
        u.print_t('Post content...')
        postid = blog.new_post(self.html_title, html_body)
        self.data.add_blog(self.file_guid, server['name'], postid, self.html_proc.get_html_time())
        pass

    def update_blog(self, blog, server):
        html_body = self.post_medias(blog, server)
        u.print_t('Post content...')
        blog.update_post(self.data.get_postid(server['name']), self.html_title, html_body)
        self.data.update_blog(self.file_guid, server['name'], self.html_proc.get_html_time())
        pass

    def post(self):
        u.print_t("Begin to post %s..." % self.html_title)
        for server in self.servers:
            try:
                self.post_blog(server)
            except pyblog.BlogError as fault:
                u.print_t('Process failure! BlogError: %s\n' % fault)
                continue
##            else :
##                u.print_t('Process failure! Unknown error.\n')
##                continue
            u.print_t('Process successfull!\n')
        self.data.write_file()
        pass

    def connect(self, server):
        u.print_t("Connect to server %s..." % server['name'])
        return self.server_class[server['system']](server['posturl'], server['username'], server['password'])

    def post_blog(self, server):
        if server['postblog'] != 'true':
            u.print_t("No post on %s because of manual closing."  %(server['name']))
            return
        flag = self.should_post_blog(server['name'])
        if flag == '0':
            u.print_t("No post on %s because of no modify."  %(server['name']))
            return
        blog = self.connect(server)
        if flag == '1':
            u.print_t("Begin new post on %s..."  %(server['name']))
            self.new_blog(blog, server)
        elif flag == '2':
            u.print_t("Begin update post on %s..."  %(server['name']))
            self.update_blog(blog, server)
        pass

    def post_medias(self, blog, server):
        flag = server['media']
        if flag == '0' :
            return self.html_body
        if flag == '1' :
            return self.upload_medias(blog, self.html_body)
        self.html_body = self.upload_medias(blog, self.html_body)
        return self.html_body

    def upload_medias(self, blog, html_body):
        for media in self.new_medias:
            if self.should_post_media(media) == '1':
                url = self.upload_media(blog, media)
                html_body = self.html_proc.update_html_body(html_body, media, url)
                self.data.update_media(self.file_guid, media, url, self.html_proc.get_media_time(media))  # update one media info to data file.
            else :
                html_body = self.html_proc.update_html_body(html_body, media, self.data.get_media_list(self.file_guid)[media]['remote_path']) # update html_body's media path
        return html_body

    def upload_media(self, blog, media):
        u.print_t("Upload media file: %s..." % media)
        return blog.upload_media(media)['url']


def usage():
    help = '''Usage:\r\n      python.exe blogpost.py html_file file_guid [config_file data_file]\r\n''';
    print(help)

def main():
    if len(sys.argv) < 3:
        usage()
        return -1

    cur_dir = os.getcwd()
    html_file = sys.argv[1]
    if html_file[-3:] == 'ziw':
        html_file = u.ziw2html(html_file)

    if len(sys.argv) == 3:  # 前面改变了当前路径为临时目录，所以配置文件要使用绝对路径
        config_file = cur_dir+ os.path.sep + 'blogconfig.xml'
        data_file = cur_dir+ os.path.sep + 'blogdata.xml'
    if len(sys.argv) == 5:
        config_file = cur_dir+ os.path.sep + sys.argv[3]  # 输入的blogconfig.xml等文件要是相对于刚开始运行时的相对路径
        data_file = cur_dir+ os.path.sep + sys.argv[4]

    if not os.path.isfile(config_file):
        printf('Config file(%s) not exist!' % config_file)
        return -1

    return BlogPost(html_file, sys.argv[2], config_file, data_file).post()

    usage()
    return -1

if   __name__  ==  "__main__":
##    cur_dir = os.getcwd()
##    ziw2html('test/Google小工具使用技巧.ziw')
##    BlogPost('index.html', '35888c3d608ba32852d2e81836c764b8', cur_dir+ os.path.sep + 'blogconfig.xml', cur_dir+ os.path.sep + 'blogdata.xml').post()
    main()