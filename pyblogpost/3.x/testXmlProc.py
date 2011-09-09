import unittest
import lxml.etree
import UserException
import XmlProc


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

    def test_get_list_of_dict(self):
        xml = XmlProc.XmlProc(in_string = self.str_children_text)
        self.assertEqual(xml.get_list_of_dict('/blog'), self.expect_children_text)
        pass

    def test_get_dict_of_dict(self):
        xml = XmlProc.XmlProc(in_string = self.str_attr_and_children_text)
        self.assertEqual(xml.get_dict_of_dict('/blog', 'name'), self.expect_attr_and_children_text)
        pass
    def test_set_root(self):
        xml = XmlProc.XmlProc()
        xml.set_root('data')
        self.assertEqual(xml.get_xml_string(), '<data/>')
    def test_add_child(self):
        xml = XmlProc.XmlProc()
        xml.set_root('data')
        xml.add_child('/data', 'child', 'text')
        self.assertEqual(xml.get_xml_string(), '<data><child>text</child></data>')
    def test_modify_child(self):
        xml = XmlProc.XmlProc()
        xml.set_root('data')
        xml.add_child('/data', 'child', 'text')
        xml.modify_node('/data/child', 'new text')
        self.assertEqual(xml.get_xml_string(), '<data><child>new text</child></data>')
    def test_add_children_list(self):
        xml = XmlProc.XmlProc()
        xml.set_root('data')
        xml.add_children('/data', 'child', [{'key1':'value1','key2':'value2'}])
        self.assertEqual(xml.get_xml_string(), '<data><child><key2>value2</key2><key1>value1</key1></child></data>')
    def test_add_children_dict(self):
        xml = XmlProc.XmlProc()
        xml.set_root('data')
        xml.add_children('/data', 'child', {'name1':{'key1_1':'value1_1','key1_2':'value1_2'}, 'name2':{'key2_1':'value2_1','key2_2':'value2_2'}}, 'name')
        self.assertEqual(xml.get_xml_string(), "<data><child name=\"name2\"><key2_2>value2_2</key2_2><key2_1>value2_1</key2_1></child><child name=\"name1\"><key1_1>value1_1</key1_1><key1_2>value1_2</key1_2></child></data>")
    pass

def base_lxml_test():
    xml=lxml.etree.fromstring(TestXmlProc.str_attr_and_children_text)
    node = xml.xpath('/blog')
    print(node[0].get('name'))
    pass


if __name__ == '__main__':
##    base_lxml_test()
    unittest.main()