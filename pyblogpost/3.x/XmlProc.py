#!/usr/bin/python
# coding=cp936
# python 3.x

import lxml.etree
import UserException


class XmlProc:
    '''
    Read/write xml compound nodes.
    '''
    def __init__(self, in_file = None, in_string = None):
        if in_file :
            self.tree = lxml.etree.parse(in_file)
        elif in_string :
            self.tree = lxml.etree.fromstring(in_string)
        else :
            #raise UserException.ParamException
            pass

    #---------------------------------------------------------------------------
    # Read xml compound nodes
    #---------------------------------------------------------------------------

    def get_list_of_dict(self, node_path):
        """
        Make nodes's list of children's tag/text dictionary.

        get_children_text
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
            list.append(self._children_dict(children))
        return list

    def get_dict_of_dict(self, node_path, attri_name):
        """
        Make nodes's dictionary of children's tag/text dictionary.

        get_attr_and_children_text
        It's a dictionary of dictionary.
        Use attr_name's value as dictionary key.
        Args:
            node_path = the nodes' XPath string, whose children to make dictionary.
        Returns:
            Dictionary of nodes' children tag/text dictionary.
        """
        try:
            nodes = self.tree.xpath(node_path)     # nodes is a list, find the nodes with attribute attr_name
        except:
            # no node_path found
            return {}
        dict = {}
        for node in nodes :
            children = node.getchildren()
            attri = node.get(attri_name)
            if attri :
                dict[attri] = self._children_dict(children)
        return dict

    def _children_dict(self, children) :
        """
        Make dictionary from children's tag/text.

        Args:
            children = children to make dictionary.
        Returns:
            Dictionary of children's tag/text.
        """
        dict = {}
        for child in children :
            dict[child.tag] = child.text
        return dict

    #---------------------------------------------------------------------------
    # Write xml compound nodes (too complex to use)
    #---------------------------------------------------------------------------
    def set_root(self, root):
        '''
        Create xml root element.

        If not give __init__ in_file and in_string parameter,
        and out_file not exist, you should set root first.
        Args:
        root = root's name.
        Returns:
        None
        '''
        ##self.tree = lxml.etree.fromstring('<'+root+'/>') # ok
        self.tree = lxml.etree.Element(root)
        pass

    def add_child(self, parent_path, child, text):
        '''
        Add node according to node_path.

        Args:
        parent_path = parent node xpath.
        child = child node to add
        Returns:
        None
        '''
        parent = self.get_one_node(parent_path)
        elem = lxml.etree.Element(child)
        elem.text = text
        parent.append(elem)
        pass

    def add_children(self, parent_path, me, children, attri_name = None):
        '''
        Add children(list of dictionary or dictionary of dictionary) as node_path's child and grandson.

        Args:
        node_path = parent node.
        children  = compound nodes(list of dictionary or dictionary of dictionary)
        Returns:
        None
        '''
        parent = self.get_one_node(parent_path)

        #children is list (with no attribute)
        if isinstance(children, list) :
            for children_dict in children:
                me_node = lxml.etree.Element(me)
                for key, value in children_dict.items():
                    elem = lxml.etree.Element(key)
                    elem.text = value
                    me_node.append(elem)
                parent.append(me_node)

        #children is dictionary (with attribute)
        elif isinstance(children, dict) :
            if not attri_name :
                raise UserException.ParamException
            for key, children_dict in children.items():
                me_node = lxml.etree.Element(me)
                me_node.set(attri_name, key)
                for key, value in children_dict.items():
                    elem = lxml.etree.Element(key)
                    elem.text = value
                    me_node.append(elem)
                parent.append(me_node)
        else :
            raise TypeError

    def del_node(self, node_path):
        '''
        Delete node and it's children.

        Args:
        node_path = node to delete.
        Returns:
        None
        '''
        raise FutureWarning

    def modify_node(self, node_path, text):
        '''
        Modify node's text to the input text.

        Args:
        node_path = node to modify.
        Returns:
        None
        '''
        node = self.get_one_node(node_path)
        node.text = text
        pass

    def get_xml_string(self):
        '''
        Get xml tree string.

        Returns:
        Return xml tree string.
        '''
        return lxml.etree.tostring(self.tree).decode()

    def get_one_node(self, path):
        '''
        Get the only node from xpath.

        Returns:
        Return the only node.
        '''
        nodes = self.tree.xpath(path)
        if len(nodes) ==0 :
            raise UserException.NotFoundException
        elif len(nodes) > 1 :
            raise UserException.TooManyNodesException
        return nodes[0]

def cdata_text(text):
    return "<![CDATA["+text+"]]>"

#module test
##XmlProc(out_file = 'd.xml')
##XmlProc()
##xml = XmlProc(out_file='a.xml')
##xml.set_root('data')
##print(xml.get_tree_string())
##xml.add_child('data', 'child', 'text')
##print(xml.get_tree_string())

##root = lxml.etree.Element('data')
##print(root)
##root1 = lxml.etree.fromstring('<data/>')
##print(root1)
##root2 = root1.xpath('/data')
##print(root2)
##html_file = lxml.etree.Element('html_file')
##root1.append(html_file)
##print(lxml.etree.tostring(root1))

###test cdata (if text includes '<' or '>', cdata is needed.'/','\' not need.)
##str = r"<data><![CDATA[te\s/t\text]]></data>"
##str2 = r"<data>te\s/t\text</data>"
##tree = lxml.etree.fromstring(str)
##nodes = tree.xpath('/data')
##print(nodes[0].text)
##tree2 = lxml.etree.fromstring(str2)
##nodes2 = tree.xpath('/data')
##print(nodes2[0].text)