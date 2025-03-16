class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        props_lst = []
        for k in self.props:
            props_lst.append(f"{k}=\"{self.props[k]}\"")
        return " " + " ".join(props_lst)
    
    def __repr__(self):
        return f"HTMLNode(tag=\"{self.tag}\" value=\"{self.value}\" children={self.children} props={self.props})"