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
        chk_str = " attr1=\"val1\""
        self.assertEqual(node.props_to_html(), chk_str)
    
    def test_props_to_html_3(self):
        node = HTMLNode(props={"attr1":"val1", "attr2":"val2", "attr3":"val3"})
        chk_str = " attr1=\"val1\" attr2=\"val2\" attr3=\"val3\""
        self.assertEqual(node.props_to_html(), chk_str)
    

    def test_leafnode_to_html(self):
        node = LeafNode("a", "link to site", {"href":"https://test.com"})
        chk_str = "<a href=\"https://test.com\">link to site</a>"
        self.assertEqual(node.to_html(), chk_str)
    

    def test_parentnode_to_html(self):
        ln1 = LeafNode("p", "this is a paragraph")
        ln2 = LeafNode("b", "bold text")

        node = ParentNode("div", [ln1, ln2], {"attr1":"value1"})
        chk_str = '<div attr1="value1"><p>this is a paragraph</p><b>bold text</b></div>'
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
    

    def test_split_nodes_image(self):
        t = TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
        self.assertEqual(repr(split_nodes_image([t])), "[TextNode(text=\"This is text with a link \" text_type=normal url=None), TextNode(text=\"to boot dev\" text_type=image url=https://www.boot.dev), TextNode(text=\" and \" text_type=normal url=None), TextNode(text=\"to youtube\" text_type=image url=https://www.youtube.com/@bootdotdev)]")
    
    def test_split_nodes_link(self):
        self.maxDiff = None
        t = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
        self.assertEqual(repr(split_nodes_link([t])), "[TextNode(text=\"This is text with a link \" text_type=normal url=None), TextNode(text=\"to boot dev\" text_type=link url=https://www.boot.dev), TextNode(text=\" and \" text_type=normal url=None), TextNode(text=\"to youtube\" text_type=link url=https://www.youtube.com/@bootdotdev)]")


    def test_text_to_textnodes(self):
        nodes = text_to_textnode("normal text **bold text** normal text 2 _italic text_ normal text 3, `code text` normal text ![image alt](https://test.com/test.jpg) normal text 4 [link text](https://test.com)")
        expected_nodes = [
            TextNode("normal text ", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode(" normal text 2 ", TextType.NORMAL),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" normal text 3, ", TextType.NORMAL),
            TextNode("code text", TextType.CODE),
            TextNode(" normal text ", TextType.NORMAL),
            TextNode("image alt", TextType.IMAGE, "https://test.com/test.jpg"),
            TextNode(" normal text 4 ", TextType.NORMAL),
            TextNode("link text", TextType.LINK, "https://test.com"),
        ]
        self.assertListEqual(nodes, expected_nodes)


    def test_markdown_to_blocks(self):
        self.maxDiff = None
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type_heading(self):
        self.maxDiff = None
        md = "## heading 2"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)
    
    def test_block_to_block_type_code(self):
        self.maxDiff = None
        md = "```code line;\ncode line;\ncode line;\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        self.maxDiff = None
        md = ">quote\n>quote\n>quote\n"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)
    
    def test_block_to_block_type_ul(self):
        self.maxDiff = None
        md = "- item\n- item\n- item"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ol(self):
        self.maxDiff = None
        md = "1. item\n2. item\n3. item"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_p(self):
        self.maxDiff = None
        md = "this is a\nnormal paragraph"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    

    def test_markdown_to_html_node(self):
        self.maxDiff = None
        md = """
### heading 3 _italic text_ heading 3

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

- item 1
- item 2
- item 3

1. item 1
2. item 2
3. item 3
"""
        chk_str = "<div><h3>heading 3 <i>italic text</i> heading 3</h3><p>This is <b>bolded</b> paragraph<br>text in a p<br>tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul><ol><li>item 1</li><li>item 2</li><li>item 3</li></ol></div>"
        self.assertEqual(markdown_to_html_node(md).to_html(), chk_str)
    
    def test_extract_title(self):
        md = "# heading 1 "
        self.assertEqual(extract_title(md), "heading 1")

if __name__ == "__main__":
    unittest.main()