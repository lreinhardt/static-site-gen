from enum import Enum
import re

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

        if self.text_type == TextType.LINK and self.url == None:
            raise ValueError("TextNode.__init__: TextType.LINK requires valid url")
        if self.text_type == TextType.IMAGE and self.url == None:
            raise ValueError("TextNode.__init__: TextType.IMAGE requires valid url")

    def __eq__(self, other):
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)
    
    def __repr__(self):
        return f"TextNode(text=\"{self.text}\" text_type={self.text_type.value} url={self.url})"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_block):
    if re.findall(r"^#{1,6}", markdown_block):
        return BlockType.HEADING

    if markdown_block.strip().startswith("```") and markdown_block.strip().endswith("```"):
        return BlockType.CODE
    
    lines = markdown_block.strip().split("\n")
    is_quote_block = True
    for l in lines:
        if not l.startswith(">"):
            is_quote_block = False
            break
    if is_quote_block:
        return BlockType.QUOTE
    
    is_ul_block = True
    for l in lines:
        if not l.startswith("- "):
            is_ul_block = False
            break
    if is_ul_block:
        return BlockType.UNORDERED_LIST
    
    is_ol_block = True
    for i in range(1, len(lines) + 1):
        if not lines[i-1].startswith(f"{i}. "):
            is_ol_block = False
            break
    if is_ol_block:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

