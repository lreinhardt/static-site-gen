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
        rstr = ""
        if self.tag == None:
            t = ""
        else:
            t = f"{self.tag}"
        
        if self.value == None:
            v = ""
        else:
            v = f"{self.value}"
        
        if self.children == None:
            c = "[]"
        else:
            c = f"{self.children}"
        if self.props == None:
            p = "{}"
        else:
            p = f"{{{self.props_to_html()}}}"

        return f"HTMLNode(tag=\"{t}\" value=\"{v}\" children={c} props={p})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

        if self.value == None:
            raise ValueError("LeafNode.__init__: value is required")
    
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

