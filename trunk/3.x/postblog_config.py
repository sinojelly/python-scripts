
import lxml.etree


def children_dic(children) :
    """
    Make dictionary from children's tag/value.

    Args:
        children = children to make dictionary.
    Returns:
        Dictionary of children's tag/value.
    """
    dic = {}
    for child in children :
        dic[child.tag] = child.text
    return dic

def get_fileserver(config_file) :
    """
    Get fileserver parameters.

    Returns:
        Dictionary of fileserver parameters(posturl/username/password).
    """
    tree = lxml.etree.parse(config_file)
    nodes = tree.xpath('/config/fileserver')
    if nodes :
        children = nodes[0].getchildren()
        return children_dic(children)

def get_blogs(config_file):
    """
    Get blogs parameters.

    list_blog[0] = [{'name':'servername', 'system':'wordpress', 'posturl':url, 'username':usr, 'password':pass, 'upload':'false'}]
    Returns:
        List of blogs parameters(system/posturl/username/password/upload) dictionary.
    """
    tree = lxml.etree.parse(config_file)
    nodes = tree.xpath('/config/blog')
    list_blog = []
    for node in nodes :
        children = node.getchildren()
        list_blog.append(children_dic(children))
    return list_blog


##print(get_blogs("postblog_config.xml"))

##print(nodes)
##print(nodes.__class__)
##print(nodes[0])
##print(nodes[0].__class__)
