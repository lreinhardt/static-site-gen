from textnode import *
import re

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
            return " " + " ".join(map(lambda i: f"{i[0]}=\"{i[1]}\"", self.props.items()))

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
            p = f"{{{self.props_to_html()[1:]}}}"

        return f"HTMLNode(tag={t} value={v} children={c} props={p})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag != None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"{self.value}"


class ParentNode(HTMLNode):

    def __init__(self, tag, children=[], props=None):
        super().__init__(tag, None, children, props)

        if tag == None:
            raise ValueError("ParentNode.__init__: tag is required")
        
        if children == None:
            self.children = []
    
    def to_html(self):
        children_html = ""
        for c in self.children:
            children_html += c.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def add_child_node(self, node):
        if not isinstance(node, LeafNode) and not isinstance(node, ParentNode):
            raise ValueError("invalid node type")
        
        self.children.append(node)


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
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for n in old_nodes:
        if n.text_type != TextType.NORMAL:
            new_nodes.append(n)
            continue
        if (n.text.count(delimiter) % 2) == 1:
            raise Exception("mismatched markdown delimiters")
        
        blocks = n.text.split(delimiter)
        for i in range(len(blocks)):
            if len(blocks[i]) == 0:
                continue
            if (i % 2) == 0:
                new_nodes.append(TextNode(blocks[i], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(blocks[i], text_type))
        
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for n in old_nodes:
        if n.text_type != TextType.NORMAL:
            new_nodes.append(n)
            continue

        imgs = extract_markdown_images(n.text)
        raw_text = n.text
        
        for alt, url in imgs:
            blks = raw_text.split(f"![{alt}]({url})", maxsplit=1)

            if len(blks[0]) > 0:
                new_nodes.append(TextNode(blks[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
        
            raw_text = blks[1]
        
        if len(raw_text) > 0:
            new_nodes.append(TextNode(raw_text, TextType.NORMAL))
        
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for n in old_nodes:
        if n.text_type != TextType.NORMAL:
            new_nodes.append(n)
            continue

        imgs = extract_markdown_links(n.text)
        raw_text = n.text
        
        for alt, url in imgs:
            blks = raw_text.split(f"[{alt}]({url})", maxsplit=1)

            if len(blks[0]) > 0:
                new_nodes.append(TextNode(blks[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
        
            raw_text = blks[1]
        
        if len(raw_text) > 0:
            new_nodes.append(TextNode(raw_text, TextType.NORMAL))
        
    return new_nodes


def text_to_textnode(text):
    init_node = TextNode(text, TextType.NORMAL)

    nodes = split_nodes_delimiter([init_node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return_blocks = []

    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
        if blocks[i] != "":
            return_blocks.append(blocks[i])

    return return_blocks


def markdown_heading_to_html_nodes(md):
    count = 0
    while md.startswith("#"):
        md = md[1:]
        count += 1
    
    if md.startswith(" "):
        md = md[1:]
    
    tns = text_to_textnode(md)
    hns = [text_node_to_html_node(tn) for tn in tns]

    return ParentNode(f"h{count}", hns)

def markdown_ol_to_html_nodes(md):
    items = md.split("<br>")
    li_items = []
    for i in range(len(items)):
        li_items.append(items[i].replace(f"{i+1}. ", ""))

    items_nodes = []
    for i in li_items:
        items_nodes.append(LeafNode("li", i))
    
    return ParentNode("ol", items_nodes)

def markdown_ul_to_html_nodes(md):
    items = md.split("<br>")
    li_items = []
    for i in range(len(items)):
        li_items.append(items[i][2:])

    items_nodes = []
    for i in li_items:
        items_nodes.append(LeafNode("li", i))
    
    return ParentNode("ul", items_nodes)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for blk in blocks:
        blk = blk.replace("\n", "<br>")
        bt = block_to_block_type(blk)
        if bt == BlockType.HEADING:
            block_nodes.append(markdown_heading_to_html_nodes(blk))
        elif bt == BlockType.CODE:
            tns = text_to_textnode(blk)
            hns = [text_node_to_html_node(tn) for tn in tns]
            block_nodes.append(ParentNode("code", hns))
        elif bt == BlockType.PARAGRAPH:
            tns = text_to_textnode(blk)
            hns = [text_node_to_html_node(tn) for tn in tns]
            block_nodes.append(ParentNode("p", hns))
        elif bt == BlockType.QUOTE:
            tns = text_to_textnode(blk)
            hns = [text_node_to_html_node(tn) for tn in tns]
            block_nodes.append(ParentNode("quote", hns))
        elif bt == BlockType.UNORDERED_LIST:
            block_nodes.append(markdown_ul_to_html_nodes(blk))
        elif bt == BlockType.ORDERED_LIST:
            block_nodes.append(markdown_ol_to_html_nodes(blk))

    root_node = ParentNode("div", block_nodes)
    
    return root_node
