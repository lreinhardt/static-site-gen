from textnode import *

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("HTMLNode.to_html: override in child classes")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        else:
            return " ".join(map(lambda i: f"{i[0]}=\"{i[1]}\"", self.props.items()))

    def __repr__(self):
        if self.tag == None:
            t = "None"
        else:
            t = f"\"{self.tag}\""
        
        if self.value == None:
            v = "None"
        else:
            v = f"\"{self.value}\""
        
        if self.children == None:
            c = "None"
        else:
            c = f"{self.children}"
        
        if self.props == None:
            p = "None"
        else:
            p = f"{{{self.props_to_html()}}}"

        return f"HTMLNode(tag={t} value={v} children={c} props={p})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag != None:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"{self.value}"


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

        if tag == None:
            raise ValueError("ParentNode.__init__: tag is required")
        
        if children == None or len(children) == 0:
            raise ValueError("ParentNode.__init__: child nodes are required")
    
    def to_html(self):
        children_html = ""
        for c in self.children:
            children_html += c.to_html()
        
        return f"<{self.tag} {self.props_to_html()}>{children_html}</{self.tag}>"


def text_node_to_html_node(textnd:TextNode):
    match textnd.text_type:
        case TextType.NORMAL:
            return LeafNode(None, textnd.text)
        case TextType.BOLD:
            return LeafNode("b", textnd.text)
        case TextType.ITALIC:
            return LeafNode("i", textnd.text)
        case TextType.CODE:
            return LeafNode("code", textnd.text)
        case TextType.LINK:
            return LeafNode("a", textnd.text, {"href":textnd.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src":textnd.url, "alt":textnd.text})