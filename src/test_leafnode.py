import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    
    def test_to_html(self):
        node = LeafNode("a", "link to site", {"href":"https://test.com"})
        chk_str = f"<a href=\"https://test.com\">link to site</a>"
        self.assertEqual(node.to_html(), chk_str)

if __name__ == "__main__":
    unittest.main()