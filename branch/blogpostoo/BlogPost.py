
import xmlrpc.client

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
        pyblog.WordPress.new_post(self.get_content(title, body))

    def update_post(self, postid, title, body):
        pyblog.WordPress.edit_post(postid, self.get_content(title, body))

    def upload_media(self, media):
        file = open(media, "rb")
        content = xmlrpc.client.Binary(file.read())  #base 64 encoding binary
        file.close()
        type = 'image/jpeg'
        if media[-3:] == 'png':
            type = 'image/png'
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
    def __init__(self, config_file, data_file, html_file, html_file_guid):
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
            return 1
        if new_time > old_time :
            return 1
        return 0

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
            return 1
        if new_time > old_time :
            return 2
        return 0

    def new_blog(self, blog, server):
        postid = blog.new_post(self.html_title, self.post_medias(blog, server))
        self.data.add_blog(self.file_guid, server['name'], postid, self.html_proc.get_html_time())
        pass

    def update_blog(self, blog, server):
        blog.update_post(self.data.get_postid(server['name']), self.html_title, self.post_medias(blog, server))
        self.data.update_blog(self.file_guid, server['name'], self.html_proc.get_html_time())
        pass

    def post(self):
        u.print_t("Begin to post %s..." % self.html_title)
        for server in self.servers:
            self.post_blog(server)
        pass

    def connect(self, server):
        u.print_t("Connect to server %s..." % server['name'])
        return self.server_class[server['system']](server['posturl'], server['username'], server['password'])

    def post_blog(self, server):
        flag = self.should_post_blog(server['name'])
        if flag == 0:
            u.print_t("No modify no post on %s.\r\n"  %(server['name']))
            return
        blog = self.connect(server)
        if flag == 1:
            u.print_t("Begin new post on %s...\r\n"  %(server['name']))
            self.new_blog(blog, server)
        elif flag == 2:
            u.print_t("Begin update post on %s...\r\n"  %(server['name']))
            self.update_blog(blog, server)
        pass

    def post_medias(self, blog, server):
        flag = server['media']
        if flag == 0 :
            return self.html_body
        if flag == 1 :
            return self.upload_medias(blog, self.html_body)
        self.html_body = self.upload_medias(blog, self.html_body)
        return self.html_body

    def upload_medias(self, blog, html_body):
        for media in self.new_medias:
            if self.should_post_media(media):
                url = self.upload_media(blog, media)
                html_body = self.html_proc.update_html_body(html_body, media, url)
                self.data.update_media(self.file_guid, media, url, self.html_proc.get_media_time(media))  #TODO: update one media info to data file.
        return html_body

    def upload_media(self, blog, media):
        u.print_t("Upload media file: %s..." % media)
        blog.upload_media(media)


def usage():
    help = '''Usage:\r\n
              python.exe blogpost.py config_file data_file html_file file_guid\r\n''';
    print(help)

def main():
    if len(sys.argv) < 5:
        usage()
        return -1
    return BlogPost(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]).post()

if   __name__  ==  "__main__":
    BlogPost('blogconfig.xml', 'blogdata.xml', 'index.html', '35888c3d608ba32852d2e81836c764b7').post()
##    main()