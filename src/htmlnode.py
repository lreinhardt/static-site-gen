class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        props_lst = []
        for k in self.props:
            props_lst.append(f"{k}=\"{self.props[k]}\"")
        return " " + " ".join(props_lst)
    
    def __repr__(self):
        return f"HTMLNode(tag=\"{self.tag}\" value=\"{self.value}\" children={self.children} props={self.props})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

        if self.value == None:
            raise ValueError("LeafNode.__init__: value is required")
    
    def to_html(self):
        if self.tag != None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
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
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

