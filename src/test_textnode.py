import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("Base TextNode", TextType.BOLD, "https://test.org")
        node2 = TextNode("Base TextNode", TextType.BOLD, "https://test.org")
        self.assertEqual(node1, node2)

    def test_not_eq1(self):
        node1 = TextNode("Base TextNode", TextType.BOLD, "https://test.org")
        node3 = TextNode("Different TextNode", TextType.BOLD, "https://test.org")
        self.assertNotEqual(node1, node3)
        
    def test_not_eq2(self):
        node1 = TextNode("Base TextNode", TextType.BOLD, "https://test.org")
        node4 = TextNode("Base TextNode", TextType.IMAGE, "https://test.org")
        self.assertNotEqual(node1, node4)
        
    def test_not_eq3(self):
        node1 = TextNode("Base TextNode", TextType.BOLD, "https://test.org")
        node5 = TextNode("Base TextNode", TextType.BOLD, "https://test_different.org")
        self.assertNotEqual(node1, node5)
    
    def test_not_eq4(self):
        node1 = TextNode("Base TextNode", TextType.BOLD, "https://test.org")
        node6 = TextNode("Base TextNode", TextType.BOLD)
        self.assertNotEqual(node1, node6)
    
    def test_repr(self):
        node4 = TextNode("Base TextNode", TextType.IMAGE, "https://test.org/test.jpg")
        chk_str = "TextNode(text=\"Base TextNode\" text_type=image url=https://test.org/test.jpg)"
        self.assertEqual(repr(node4), chk_str)



if __name__ == "__main__":
    unittest.main()