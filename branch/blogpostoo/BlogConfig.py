

import lxml.etree
import UserException


class BlogConfig:
    def __init__(self, file = None, string = None):
        if file :
            tree = lxml.etree.parse(file)
        elif string :
            tree = lxml.etree.fromstring(string)
        else :
            raise UserException.ParamException
        self.blogNode = tree.xpath('/config/blog')
        self.fileserverNode = tree.xpath('/config/fileserver')

        self.fileserver = {}
        self.blogs = []

    def get_fileserver(self) :
        """
        Get fileserver parameters.

        Returns:
            Dictionary of fileserver parameters(posturl/username/password).
        """
        if self.fileserver:
            return self.fileserver

        self.fileserver = {}
        if self.fileserverNode:
            children = self.fileserverNode[0].getchildren()
            self.fileserver = self._children_dic(children)

        return self.fileserver

    def get_blogs(self):
        """
        Get blogs parameters.

        list_blog[0] = [{'name':'servername', 'system':'wordpress', 'posturl':url, 'username':usr, 'password':pass, 'upload':'false'}]
        Returns:
            List of blogs parameters(system/posturl/username/password/upload) dictionary.
        """
        if self.blogs:
            return self.blogs

        self.blogs = []
        for node in self.blogNode :
            children = node.getchildren()
            self.blogs.append(self._children_dic(children))
        return self.blogs

    def _children_dic(self, children) :
        """
        Make dictionary from children's tag/text.

        Args:
            children = children to make dictionary.
        Returns:
            Dictionary of children's tag/text.
        """
        dic = {}
        for child in children :
            dic[child.tag] = child.text
        return dic


##raise UserException.ParamException
##BlogConfig()
