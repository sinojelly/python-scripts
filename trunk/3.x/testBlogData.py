#!/usr/bin/python
# coding=cp936
# python 3.x

import unittest
import BlogData
import UserException

import lxml.etree


class TestBlogData(unittest.TestCase):
    data_xml1 = \
    '''
    <data>
        <html_file wk_file_guid="123">
                <media>
                    <file local_path="index123/a.jpg">
                        <remote_path>http://sinojelly.20x.cc/index123/a.jpg</remote_path>
                        <file_hash>2010.2.18.00:40</file_hash>
                    </file>
                    <file local_path="index123/b.png">
                        <remote_path>http://sinojelly.20x.cc/index123/b.png</remote_path>
                        <file_hash>2010.2.18.00:30</file_hash>
                    </file>
                </media>
        </html_file>
    </data>
    '''
    data_xml2 = \
    '''
    <data>
        <html_file wk_file_guid="123">
                <media>
                    <file local_path="index123/a.jpg">
                        <remote_path>http://sinojelly.20x.cc/index123/a.jpg</remote_path>
                        <file_hash>2010.2.18.00:40</file_hash>
                    </file>
                    <file local_path="index123/b.png">
                        <remote_path>http://sinojelly.20x.cc/index123/b.png</remote_path>
                        <file_hash>2010.2.18.00:30</file_hash>
                    </file>
                </media>
                <blog name="sinojelly.20x.cc">
                    <postid>10</postid>
                    <file_hash>2010.2.18.00:30</file_hash>
                </blog>
                <blog name="sinojelly.dreamhost">
                    <postid>20</postid>
                    <file_hash>2010.2.18.00:30</file_hash>
                </blog>
        </html_file>
            <html_file wk_file_guid="456">
                <media>
                    <file local_path="index456/a.jpg">
                        <remote_path>http://sinojelly.20x.cc/index456/a.jpg</remote_path>
                        <file_hash>2010.2.18.00:40</file_hash>
                    </file>
                    <file local_path="index456/b.png">
                        <remote_path>http://sinojelly.20x.cc/index456/b.png</remote_path>
                        <file_hash>2010.2.18.00:30</file_hash>
                    </file>
                </media>
                <blog name="sinojelly.20x.cc">
                    <postid>30</postid>
                    <file_hash>2010.2.18.00:30</file_hash>
                </blog>
                <blog name="sinojelly.dreamhost">
                    <postid>40</postid>
                    <file_hash>2010.2.18.00:30</file_hash>
                </blog>
            </html_file>
    </data>
    '''
    data_xml_err = \
    '''<data>
            <html_file wk_file_guid="123">
                <media>
                    <file local_path="index123/a.jpg">
                        <remote_path>http://sinojelly.20x.cc/index123/a.jpg</remote_path>
                        <file_hash>2010.2.18.00:40</file_hash>
                    </file>
                    <file local_path="index123/b.png">
                        <remote_path>http://sinojelly.20x.cc/index123/b.png</remote_path>
                        <file_hash>2010.2.18.00:30</file_hash>
                    </file>
                </media>
                <blog name="sinojelly.20x.cc">
                    <postid>10</postid>
                    <file_hash>2010.2.18.00:30</file_hash>
                </blog>
                <blog name="sinojelly.dreamhost">
                    <postid>20</postid>
                    <file_hash>2010.2.18.00:30</file_hash>
                </blog>
            </html_file>
            <html_file wk_file_guid="456">
                <media>
                    <file local_path="index456/a.jpg">
                        <remote_path>http://sinojelly.20x.cc/index456/a.jpg</remote_path>
                        <file_hash>2010.2.18.00:40</file_hash>
                    </file>
                    <file local_path="index456/b.png">
                        <remote_path>http://sinojelly.20x.cc/index456/b.png</remote_path>
                        <file_hash>2010.2.18.00:30</file_hash>
                    </file>
                </media>
                <blog name="sinojelly.20x.cc">
                    <postid>30</postid>
                    <file_hash>2010.2.18.00:30</file_hash>
                </blog>
                <blog name="sinojelly.dreamhost">
                    <postid>40</postid>
                    <file_hash>2010.2.18.00:30</file_hash>
                </blog>
            </html_file>
        <data>'''
    expect_media_list = {\
        "index123/a.jpg":{
        'remote_path':'http://sinojelly.20x.cc/index123/a.jpg',
        'file_hash':'2010.2.18.00:40'},
        "index123/b.png":{
        'remote_path':'http://sinojelly.20x.cc/index123/b.png',
        'file_hash':'2010.2.18.00:30'},
        }
    media_update = {\
        "index123/a.jpg":{
        'remote_path':'http://sinojelly.20x.cc/index123/a11.jpg',
        'file_hash':'2010.2.18.10:40'},
        "index123/c.png":{
        'remote_path':'http://sinojelly.20x.cc/index123/c.png',
        'file_hash':'2010.3.18.00:30'},
        }

    expect_blogs = { \
        "sinojelly.20x.cc":{
        'postid':'10',
        'file_hash':'2010.2.18.00:30'},
        "sinojelly.dreamhost":{
        'postid':'20',
        'file_hash':'2010.2.18.00:30'},
    }

    expect_blogs_after_add = { \
        "sinojelly.20x.cc":{
        'postid':'10',
        'file_hash':'2010.2.18.00:30'},
        "sinojelly.dreamhost":{
        'postid':'20',
        'file_hash':'2010.2.18.00:30'},
        "sinojellycn.live.space":{
        'postid':'100',
        'file_hash':'2020.1.1.10:30'},
    }

    expect_blogs_after_update = { \
        "sinojelly.20x.cc":{
        'postid':'10',
        'file_hash':'2010.2.18.00:30'},
        "sinojelly.dreamhost":{
        'postid':'20',
        'file_hash':'2010.2.18.00:30'},
        "sinojellycn.live.space":{
        'postid':'100',
        'file_hash':'2010.1.1.10:30'},
    }

    def test_get_media_list_1(self):
        data = BlogData.BlogData(string = self.data_xml1)
        media_list = data.get_media_list('123')
        self.assertEqual(self.expect_media_list, media_list)

    def test_get_media_list_2(self):
        data = BlogData.BlogData(string = self.data_xml2)
        media_list = data.get_media_list('123')
        self.assertEqual(self.expect_media_list, media_list)

    def test_get_blogs(self):
        data = BlogData.BlogData(string = self.data_xml2)
        blogs = data.get_blogs('123')
        self.assertEqual(self.expect_blogs, blogs)

    def test_add_blog(self):
        data = BlogData.BlogData(string = self.data_xml2)
        data.add_blog('123', "sinojellycn.live.space", '100', '2020.1.1.10:30')
        blogs = data.get_blogs('123')
        self.assertEqual(self.expect_blogs_after_add, blogs)

    def test_update_blog(self):
        data = BlogData.BlogData(string = self.data_xml2)
        data.add_blog('123', "sinojellycn.live.space", '100', '2020.1.1.10:30')
        data.update_blog('123', "sinojellycn.live.space", '2010.1.1.10:30')
        blogs = data.get_blogs('123')
        self.assertEqual(self.expect_blogs_after_update, blogs)

    def test_update_media_files(self):
        data = BlogData.BlogData(string = self.data_xml2)
        data.update_media_files('123', self.media_update)
        media_list = data.get_media_list('123')
        self.assertEqual(self.media_update, media_list)

    expect_update_media = {\
        "index123/a.jpg":{
        'remote_path':'http://sinojelly.20x.cc/index123/a.jpg',
        'file_hash':'2010.2.18.00:40'},
        "index123/b.png":{
        'remote_path':'http://localhost/a.png',
        'file_hash':'2010.4.18.00:40'},
        }
    def test_update_media(self):
        data = BlogData.BlogData(string = self.data_xml2)
        media_list = data.get_media_list('123')
        self.assertEqual(self.expect_media_list, media_list)
        data.update_media('123', 'index123/b.png', 'http://localhost/a.png', '2010.4.18.00:40')
        media_list = data.get_media_list('123')
        self.assertEqual(self.expect_update_media, media_list)
    def test_update_node_text(self):
        data = BlogData.BlogData(string = '<father/>')
        data.update_node_text('/father', 'me', 'me text')
        self.assertEqual(lxml.etree.tostring(data.tree).decode(), '<father><me>me text</me></father>')


if __name__ == '__main__':
    unittest.main()