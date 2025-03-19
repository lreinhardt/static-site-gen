import unittest

from htmlnode import *
from textnode import *


class Testhtmlode(unittest.TestCase):

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
    

    def test_leafnode_to_html(self):
        node = LeafNode("a", "link to site", {"href":"https://test.com"})
        chk_str = "<a href=\"https://test.com\">link to site</a>"
        self.assertEqual(node.to_html(), chk_str)
    

    def test_parentnode_to_html(self):
        ln1 = LeafNode("p", "this is a paragraph")
        ln2 = LeafNode("b", "bold text")

        node = ParentNode("div", [ln1, ln2], {"attr1":"value1"})
        chk_str = '<div attr1="value1"><p >this is a paragraph</p><b >bold text</b></div>'
        self.assertEqual(node.to_html(), chk_str)
    

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
    

    def test_split_nodes_delimiter_1(self):
        tn = TextNode("normal text 1 **bold_text** normal text 2", TextType.NORMAL)
        nn = split_nodes_delimiter([tn], "**", TextType.BOLD)
        self.assertEqual(repr(nn), repr([TextNode("normal text 1 ", TextType.NORMAL), TextNode("bold_text", TextType.BOLD), TextNode(" normal text 2", TextType.NORMAL)]))
    
    def test_split_nodes_delimiter_2(self):
        tn = TextNode("normal text 1 `code text` normal text 2", TextType.NORMAL)
        nn = split_nodes_delimiter([tn], "`", TextType.CODE)
        self.assertEqual(repr(nn), repr([TextNode("normal text 1 ", TextType.NORMAL), TextNode("code text", TextType.CODE), TextNode(" normal text 2", TextType.NORMAL)]))

    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        " and this is another ![image2](https://i.imgur.com/jsdTZks.png)")
        
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),
                              ("image2", "https://i.imgur.com/jsdTZks.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://test.com)")
        self.assertListEqual([("link", "https://test.com")], matches)


if __name__ == "__main__":
    unittest.main()