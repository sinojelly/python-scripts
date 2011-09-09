#!/usr/bin/python
# coding=cp936
# python 3.x

import re
import os

import Utility as u

class HtmlProc:
    def __init__(self, file):
        self.media_files = []
        self.media_hashs = {}
        self.init_html_content(file)
        self.init_media_files()
        self.html_hash = u.get_file_hash(file)

    def get_html_title(self):
        return self.html_title

    def get_html_body(self):
        '''Get html body without media path replaced.'''
        return self.html_body

    def get_html_hash(self):
        return self.html_hash

    def get_media_hash(self, media):
        return self.media_hashs[media]

    def get_media_files(self):
        return self.media_files

    def update_html_body(self, html_body, media, url):
        ##global global_index
        ##u.save_file(u.tool_dir(True)+"debug_html_body_%d.txt" % global_index, "[media]"+media + "\n[url]" + url+"\n"+ html_body)
        ##global_index = global_index + 1
        #p = re.compile(media,re.S|re.I) # some times not work.
        #return p.sub(url, html_body)  #replace html's img path to remote url.
        return html_body.replace(media, url) # this is ok!
        #return self.string_replace(html_body, media, url) # this is ok, but ulgly

    def string_replace(self, string, old, new):
        temp = ""
        index = string.find(old)
        while index >= 0:
            temp += string[0:index]
            temp += new
            ##if (index+len(old) < len(string)):
            #print("find at: %d" % index)
            ##print(len(string))
            temp += string[index+len(old) :]
            string = temp
            index = string.find(old)
            temp = ""
        return string

    def init_media_files(self):
        '''Get list of media files path.'''

        # use re.I to ignore case.
        u.print_t("Get media list...")
        ##p = re.compile(r'''.*?<.*?IMG.*?src\s*=\s*"(.*?)".*?>.*?''',re.S|re.I)   #some times, this is very slow.#should use first and last .*
        #p = re.compile(r'''<IMG.*?src="(.*?)".*?>''',re.S|re.I)
        p = re.compile(r'''<IMG.*?src="(.*?)"''',re.S|re.I)

        iterator = p.finditer(self.html_body)
        for match in iterator:
            media = match.group(1)
            if os.path.isfile(media):  # maybe file not exist, should ignore
                self.media_files.append(media)
                self.media_hashs[media] = u.get_file_hash(media)

    def init_html_content(self, filename):
        u.print_t("Parsing "+filename+" content...")

        # open html file, it's Unicode encoding.
        html_file = open(filename, encoding='utf-16')
        html_content = html_file.read()
        html_file.close()

        #remove \r\n and \n, re.S indicate that . matches\n
        p = re.compile(r"\r?\n",re.S)
        html_content = p.sub("",html_content)

        #remove the head
        p = re.compile(r'.*<TITLE>(.*)</TITLE>(.*<BODY>)?',re.S | re.I)
        m = p.match(html_content)
        if m:
            self.html_title = m.group(1)
            self.html_body = p.sub("",html_content)
        else:
            self.html_title = filename
            self.html_body = html_content

        #remove the tail
        p = re.compile(r'</BODY>(.*</HTML>)?',re.S | re.I) # if no body, but have html, there will be a problem
        self.html_body = p.sub("",self.html_body)


##global_index = 0