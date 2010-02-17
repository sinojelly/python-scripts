

import lxml.etree
import UserException


class XmlProc:
    def __init__(self, in_file = None, in_string = None, out_file = None):
        if in_file :
            self.tree = lxml.etree.parse(in_file)
        elif in_string :
            self.tree = lxml.etree.fromstring(in_string)
        elif out_file:
            raise FutureWarning
        else :
            raise UserException.ParamException

    def get_children_text(self, node_path):
        """
        Make nodes's list of children's tag/text dictionary.

        It's a list of dictionary.
        Args:
            node_path = the nodes' XPath string, whose children to make dictionary.
        Returns:
            List of nodes' children tag/text dictionary.
        """
        nodes = self.tree.xpath(node_path)     # nodes is a list
        list = []
        for node in nodes :
            children = node.getchildren()
            list.append(self._children_dic(children))
        return list

    def get_attr_and_children_text(self, node_path, attr_name):
        """
        Make nodes's dictionary of children's tag/text dictionary.

        It's a dictionary of dictionary.
        Args:
            node_path = the nodes' XPath string, whose children to make dictionary.
        Returns:
            Dictionary of nodes' children tag/text dictionary.
        """
        nodes = self.tree.xpath(node_path)     # nodes is a list, find the nodes with attribute attr_name
        dic = {}
        for node in nodes :
            children = node.getchildren()
            attr = node.get(attr_name)
            if attr :
                dic[attr] = self._children_dic(children)
        return dic

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


#module test
##XmlProc(out_file = 'd.xml')
##XmlProc()
