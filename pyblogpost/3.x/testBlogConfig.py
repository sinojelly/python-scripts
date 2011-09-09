import unittest
import BlogConfig
import UserException


class TestBlogConfig(unittest.TestCase):
    str_xml = \
    '''<config>
            <fileserver>
                <name>blog.sinojelly.dreamhosters.com</name>
                <system>wordpress</system>
                <posturl>https://storage.msn.com/storageservice/MetaWeblog.rpc</posturl>
                <username>sinojellycn</username>
                <password>123456</password>
                <postblog>true</postblog>
            </fileserver>
            <blog>
                <name>sinojelly.20x.cc</name>
                <system>wordpress</system>
                <posturl>http://sinojelly.20x.cc/xmlrpc.php</posturl>
                <username>admin</username>
                <password>654321</password>
                <upload>false</upload>
            </blog>
        </config>'''
    expect_fileserver = [{\
        'name':'blog.sinojelly.dreamhosters.com',
        'system':'wordpress',
        'posturl':'https://storage.msn.com/storageservice/MetaWeblog.rpc',
        'username':'sinojellycn',
        'password':'123456',
        'postblog':'true',
        }]
    expect_blogs = [{\
        'name':'sinojelly.20x.cc',
        'system':'wordpress',
        'posturl':'http://sinojelly.20x.cc/xmlrpc.php',
        'username':'admin',
        'password':'654321',
        'upload':'false',
        }]
    def test_get_fileserver_and_blogs(self):
        config = BlogConfig.BlogConfig(string = self.str_xml)
        fileserver = config.get_fileserver()
        blogs = config.get_blogs()
        self.assertEqual(self.expect_fileserver, fileserver)
        self.assertEqual(self.expect_blogs, blogs)

    def test_init_no_param(self):
        self.assertRaises(UserException.ParamException, BlogConfig.BlogConfig)


if __name__ == '__main__':
    unittest.main()