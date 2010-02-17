

import WizKnowedge
import BlogConfig
import BlogData

class BlogDataX(BlogData):
    '''encapsulation complex data structure'''
    def __init__(self, guid, file):
        BlogData.__init__(in_file = file)
        self.medias = BlogData.get_media_list(guid)
        self.blogs = BlogData.get_blogs(guid)

    def get_blog_time(self, blog_name):
        blog = self.blogs[blog_name]   #TODO: if dict has no key names blog_name, it is None?
        if blog:
            return blog['modify_time']

    def get_media_time(self, media_name):
        media = self.medias[media_name]
        if media:
            return media['modify_time']
    pass


class BlogPost:
    def __init__(self, config_file, data_file, wk_file, wk_file_guid):
        self.wk_obj = WizKnowedge.WizKnowedge(wk_file)
        self.file_guid = wk_file_guid
        self.config = BlogConfig.BlogConfig(in_file = config_file)
        self.data = BlogDataX.BlogDataX(in_file = data_file)
        self.new_medias = self.wk_obj.get_media_files()
        self.old_medias = self.data.medias
        self.all_medias = []
        fileserver = self.config.get_fileserver()
        blogs = self.config.get_blogs()
        self.servers = [fileserver[0]]
        for blog in blogs :
            self.servers.append(blog)
        pass

    def should_post_media(self, file, time):
        '''Wither the blog should to post/update this article/media.

        If article not modified, but media modified, the media should post.
        Returns:
        0 --  not post
        1 --  new post
        '''
        new_time = self.wk_obj.get_media_time(file)
        old_time = self.data.get_media_time(file)  #TODO: time compare
        pass
    def should_post_blog(self, blog_name):
        '''Wither the blog should to post/update this article/media.

        If article not modified, but media modified, the media should post.
        Returns:
        0 --  not post
        1 --  new post
        2 --  update post
        '''
        new_time = self.wk_obj.get_html_time()
        old_time = self.data.get_blog_time(blog_name)  #TODO: time compare
        pass

    def new_blog(self, blog, html_body):
        pass

    def update_blog(self, blog, html_body):
        pass
    def post(self):
        for server in self.servers:
            blog = self.connect(server)
            self.post_blog(blog, server, self.post_medias(blog, server))
        pass
    def connect(self, server):
        pass
    def post_blog(self, blog, server, html_body):
        flag = self.should_post_blog(server['name'])
        if flag == 0:
            return
        elif flag == 1:
            self.new_blog(blog, html_body)
        elif flag == 2:
            self.update_blog(blog, html_body)
        pass
    def post_medias(self, blog, server):
        flag = server['media']
        if flag == 0 :
            return self.html_body
        self.upload_medias(blog)
        if flag == 1 :
            return self.update_html_body()
        self.html_body = self.update_html_body()
        return self.html_body

    def upload_medias(blog):
        for media in self.new_medias:
            self.upload_media(blog, media)
        pass
    def upload_media(self, blog, media):
        '''Update media's remote url.'''
        pass
    pass