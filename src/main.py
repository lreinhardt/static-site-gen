import textnode
import htmlnode


def text_node_to_html_node(textnd:textnode.TextNode):
    match textnd.text_type:
        case textnode.TextType.NORMAL:
            return htmlnode.LeafNode(None, textnd.text)
        case textnode.TextType.BOLD:
            return htmlnode.LeafNode("b", textnd.text)
        case textnode.TextType.ITALIC:
            return htmlnode.LeafNode("i", textnd.text)
        case textnode.TextType.CODE:
            return htmlnode.LeafNode("code", textnd.text)
        case textnode.TextType.LINK:
            return htmlnode.LeafNode("a", textnd.text, {"href":textnd.url})
        case textnode.TextType.IMAGE:
            return htmlnode.LeafNode("a", None, {"src":textnd.url, "alt":textnd.text})


