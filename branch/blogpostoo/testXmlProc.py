import unittest
import lxml.etree
import UserException


class TestXmlProc(unittest.TestCase):
    str_children_text = \
    '''
    <blog>
        <name>sinojelly.20x.cc</name>
        <system>wordpress</system>
        <posturl>http://sinojelly.20x.cc/xmlrpc.php</posturl>
        <username>admin</username>
        <password>654321</password>
        <upload>false</upload>
    </blog>
    '''
    expect_children_text = [{\
        'name':'sinojelly.20x.cc',
        'system':'wordpress',
        'posturl':'http://sinojelly.20x.cc/xmlrpc.php',
        'username':'admin',
        'password':'654321',
        'upload':'false',
        }]

    str_attr_and_children_text = \
    '''
    <blog name="sinojelly.20x.cc">
        <system>wordpress</system>
        <posturl>http://sinojelly.20x.cc/xmlrpc.php</posturl>
        <username>admin</username>
        <password>654321</password>
        <upload>false</upload>
    </blog>
    '''
    expect_attr_and_children_text = {}
    expect_attr_and_children_text['sinojelly.20x.cc'] = {\
        'system':'wordpress',
        'posturl':'http://sinojelly.20x.cc/xmlrpc.php',
        'username':'admin',
        'password':'654321',
        'upload':'false',
        }

    def test_get_children_text(self):
        xml = XmlProc.XmlProc(in_string = self.str_children_text)
        self.assertEqual(xml.get_children_text('/blog'), self.expect_children_text)
        pass

    def test_get_attr_and_children_text(self):
        xml = XmlProc.XmlProc(in_string = self.str_attr_and_children_text)
        self.assertEqual(xml.get_attr_and_children_text('/blog', 'name'), self.expect_attr_and_children_text)
        pass
    pass

def base_lxml_test():
    xml=lxml.etree.fromstring(TestXmlProc.str_attr_and_children_text)
    node = xml.xpath('/blog')
    print(node[0].get('name'))
    pass


if __name__ == '__main__':
##    base_lxml_test()
    unittest.main()