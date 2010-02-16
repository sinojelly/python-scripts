
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

def get_blogs():
    """
    Get blogs parameters.

    dic_blog[blog_name] = {'system':'wordpress', 'posturl':url, 'username':usr, 'password':pass, 'upload':'false'}
    node.items() is : [('name', 'sinojelly.20x.cc')]
    node.items()[0][1] is the real name.
    Returns:
        Dictionary of blogs parameters(system/posturl/username/password/upload) dictionary.
    """
    tree = lxml.etree.parse(config_file)
    nodes = tree.xpath('/config/blog')
    dic_blog = {}
    for node in nodes :
        children = node.getchildren()
        dic_blog[node.items()[0][1]] = children_dic(children)
    return dic_blog


##print(get_fileserver())

##print(nodes)
##print(nodes.__class__)
##print(nodes[0])
##print(nodes[0].__class__)
