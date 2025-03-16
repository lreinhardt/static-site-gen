import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    
    def test_to_html(self):
        ln1 = LeafNode("p", "this is a paragraph")
        ln2 = LeafNode("b", "bold text")
        ln3 = LeafNode(None, "normal text")
        ln4 = LeafNode("p", "this is a paragraph")

        node = ParentNode("div", [ln1, ln2, ln3, ln4], {"attr1":"value1"})
        chk_str = f"<div attr1=\"value1\"><p>this is a paragraph</p><b>bold text</b>normal text<p>this is a paragraph</p></div>"
        self.assertEqual(node.to_html(), chk_str)

if __name__ == "__main__":
    unittest.main()