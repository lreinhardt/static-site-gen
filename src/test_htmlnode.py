import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import *


class Testhtmlode(unittest.TestCase):

    ### HTMLNode
    def test_repr_1(self):
        node = HTMLNode(None, None, None, None)
        chk_str = 'HTMLNode(tag=None value=None children=None props=None)'
        self.assertEqual(repr(node), chk_str)
    
    def test_repr_2(self):
        node = HTMLNode("p", "test content", None, {"attr1":"val1", "attr2":"val2"})
        chk_str = 'HTMLNode(tag="p" value="test content" children=None props={attr1="val1" attr2="val2"})'
        self.assertEqual(repr(node), chk_str)
    
    def test_repr_3(self):
        node0 = HTMLNode(None, None, None, None)
        node1 = HTMLNode("p", "test content", [node0, node0, node0], {"attr1":"val1", "attr2":"val2"})
        chk_str = 'HTMLNode(tag="p" value="test content" children=[HTMLNode(tag=None value=None children=None props=None), HTMLNode(tag=None value=None children=None props=None), HTMLNode(tag=None value=None children=None props=None)] props={attr1="val1" attr2="val2"})'
        self.assertEqual(repr(node1), chk_str)
    
    def test_props_to_html_1(self):
        node = HTMLNode()
        chk_str = ""
        self.assertEqual(node.props_to_html(), chk_str)

    def test_props_to_html_2(self):
        node = HTMLNode(props={"attr1":"val1"})
        chk_str = "attr1=\"val1\""
        self.assertEqual(node.props_to_html(), chk_str)
    
    def test_props_to_html_3(self):
        node = HTMLNode(props={"attr1":"val1", "attr2":"val2", "attr3":"val3"})
        chk_str = "attr1=\"val1\" attr2=\"val2\" attr3=\"val3\""
        self.assertEqual(node.props_to_html(), chk_str)
    
    ### LeafNode
    def test_leafnode_to_html(self):
        node = LeafNode("a", "link to site", {"href":"https://test.com"})
        chk_str = "<a href=\"https://test.com\">link to site</a>"
        self.assertEqual(node.to_html(), chk_str)
    
    ### ParentNode
    def test_parentnode_to_html(self):
        ln1 = LeafNode("p", "this is a paragraph")
        ln2 = LeafNode("b", "bold text")

        node = ParentNode("div", [ln1, ln2], {"attr1":"value1"})
        chk_str = '<div attr1="value1"><p >this is a paragraph</p><b >bold text</b></div>'
        self.assertEqual(node.to_html(), chk_str)
    
    ### text_node_to_html_node
    def test_text_node_to_html_node_1(self):
        tn1 = TextNode("normal content", TextType.NORMAL)
        nd1 = LeafNode(None, "normal content")
        self.assertEqual(repr(nd1), repr(text_node_to_html_node(tn1)))
    
    def test_text_node_to_html_node_2(self):
        tn1 = TextNode("bold content", TextType.BOLD)
        nd1 = LeafNode("b", "bold content")
        self.assertEqual(repr(nd1), repr(text_node_to_html_node(tn1)))
    
    def test_text_node_to_html_node_3(self):
        tn1 = TextNode("italic content", TextType.ITALIC)
        nd1 = LeafNode("i", "italic content")
        self.assertEqual(repr(nd1), repr(text_node_to_html_node(tn1)))
    
    def test_text_node_to_html_node_4(self):
        tn1 = TextNode("code content", TextType.CODE)
        nd1 = LeafNode("code", "code content")
        self.assertEqual(repr(nd1), repr(text_node_to_html_node(tn1)))
    
    def test_text_node_to_html_node_5(self):
        tn1 = TextNode("link", TextType.LINK, "https://test.com")
        nd1 = LeafNode("a", "link", {"href":"https://test.com"})
        self.assertEqual(repr(nd1), repr(text_node_to_html_node(tn1)))
    
    def test_text_node_to_html_node_6(self):
        tn1 = TextNode("image", TextType.IMAGE, "https://test.com/test.jpg")
        nd1 = LeafNode("img", None, {"src":"https://test.com/test.jpg", "alt":"image"})
        self.assertEqual(repr(nd1), repr(text_node_to_html_node(tn1)))

if __name__ == "__main__":
    unittest.main()