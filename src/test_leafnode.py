import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    
    def test_to_html(self):
        tag = "a"
        val = "link to site"
        props = {"href":"https://test.com"}

        node = LeafNode(tag, val, props)
        chk_str = f"<{tag} href=\"https://test.com\">{val}</{tag}>"
        self.assertEqual(node.to_html(), chk_str)

if __name__ == "__main__":
    unittest.main()