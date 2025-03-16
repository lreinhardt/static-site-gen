import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        tag = "p"
        val = "test content"
        children = None
        props = {"attr1":"val1", "attr2":"val2"}

        node = HTMLNode(tag, val, children, props)
        chk_str = f"HTMLNode(tag=\"{tag}\" value=\"{val}\" children={children} props={props})"

        self.assertEqual(repr(node), chk_str, f"\n{node}\n!=\n{chk_str}")
    
    def test_props_to_html1(self):
        tag = "p"
        val = "test content"
        children = None
        props = {"attr1":"val1", "attr2":"val2"}

        node = HTMLNode(tag, val, children, props)
        chk_str = f" attr1=\"val1\" attr2=\"val2\""
        self.assertEqual(node.props_to_html(), chk_str)

    def test_props_to_html2(self):
        tag = "div"
        val = "https://test.com/"
        children = None
        props = {"attr3":"val3", "attr4":"val4"}

        node = HTMLNode(tag, val, children, props)
        chk_str = f" attr3=\"val3\" attr4=\"val4\""
        self.assertEqual(node.props_to_html(), chk_str)
    
    def test_to_html(self):
        tag = "a"
        val = "link to site"
        props = {"href":"https://test.com"}

        node = LeafNode(tag, val, props)
        chk_str = f"<{tag} href=\"https://test.com\">{val}</{tag}>"
        self.assertEqual(node.to_html(), chk_str)

if __name__ == "__main__":
    unittest.main()