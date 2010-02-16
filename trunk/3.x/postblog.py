#!/usr/bin/python
# coding=cp936
# python 3.x
#
# history:
# version 1.0
# 2010.2.15 support convert wizknowedge html file index.html to body only content.
# 2010.2.15 support wordpress new post, including upload media file.
# 2010.2.16 support get title from html file.
#
#

import xmlrpc.client
import pyblog
import re
import sys


def usage():
    help = '''Usage:\r\n
              python.exe postblog.py posturl username password filename\r\n''';
    print(help)


def get_html_content(filename):
	#打开带图的html文件(Unicode编码)
	html_file = open(filename, encoding='utf-16')
	html_file_content = html_file.read()
	html_file.close()

	#删除\r\n和\n, re.S表示.能匹配\n
	p = re.compile(r"\r?\n",re.S)
	html_file_content = p.sub("",html_file_content)

	#去掉头
	p = re.compile(r'<!DOCTYPE HTML PUBLIC.*<TITLE>(.*)</TITLE>.*<BODY>',re.S)
	html_file_title = p.match(html_file_content).group(1)
	html_file_body = p.sub("",html_file_content)

	#去掉尾
	p = re.compile(r'</BODY>.*</HTML>',re.S)
	html_file_body = p.sub("",html_file_body)
	return html_file_title, html_file_body

def upload_img(blog, imgname):
	file = open(imgname, "rb")
	content = xmlrpc.client.Binary(file.read())  #base 64 encoding binary
	file.close()
	type = 'image/jpeg'
	if imgname[-3:] == 'png':
		type = 'image/png'
	media_obj = {'name':imgname, 'type':type, 'bits':content}
	return blog.new_media_object(media_obj)

def proc_imgs(blog, content):
	#大小写忽略，也可以用re.I
	p = re.compile(r'''.*?<.*?IMG.*?src\s*=\s*"(.*?)".*?>.*?''',re.S|re.I)  #必须有前后的.*
	img_list = []
	iterator = p.finditer(content)
	for match in iterator:
		img_list.append(match.group(1))
		imgurl = upload_img(blog, match.group(1))
		p = re.compile(match.group(1),re.S|re.I)
		content = p.sub(imgurl['url'], content)  #替换html文件中的img图片路径为网络路径
	return content

def post_test(blog):
	print(blog.list_methods2());
	print(blog.method_help('metaWeblog.newPost'))
	print(blog.method_signature('metaWeblog.newPost'))
	print(blog.get_capabilities())
	print(blog.method_signature('metaWeblog.newMediaObject'))
	print(blog.get_recent_posts());

def post_blog(posturl, username, password, filename):
	blog = pyblog.WordPress(posturl, username, password)

	html_file_title, html_file_body = get_html_content(filename)
	html_file_body = proc_imgs(blog, html_file_body)

	content = {"description":html_file_body, "title":html_file_title}
	new_id = blog.new_post(content)
	print ("Post successful. postid: " + new_id)
	return new_id


def main(posturl, username, password, filename):
    return post_blog(posturl, username, password, filename)



if   __name__  ==  "__main__":
    if len(sys.argv) < 5:
        usage()
    print(sys.argv[1])
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])



#test blog
##blog = pyblog.WordPress(posturl, username, password)
##post_test(blog)

#test get html title
##title, body = get_html_content("test/index.html")
##print(title)

