import textnode
import htmlnode

hn = htmlnode.HTMLNode("a", "TEST", None, {"href":"https://test.com", "target":"blank_"})
ln = htmlnode.LeafNode("a", "this is a link", {"href":"https://test.com"})
print(ln.to_html())