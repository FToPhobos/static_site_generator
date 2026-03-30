from enum import Enum
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes
from htmlnode import ParentNode

def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")

    for block in blocks:
        strip_block = block.strip()
        if not strip_block:
            continue
        else:
            result.append(strip_block)

    return result


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif lines[0].startswith("```") and lines[-1].startswith("```"):
            return BlockType.CODE

    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    elif block.startswith("1. "):
        for index, line in enumerate(lines):
            if not line.startswith(f"{index + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.OLIST

    else:
        return BlockType.PARAGRAPH

    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_block = block_to_html_node(block)
        children.append(html_block)
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    new_text_nodes = text_to_textnodes(text)
    result = []
    for nodes in new_text_nodes:
        html_node = text_node_to_html_node(nodes)
        result.append(html_node)
    return result

def paragraph_to_html_node(block):
    lines = block.split("\n")
    para = " ".join(line.strip() for line in lines)
    result = text_to_children(para)
    return ParentNode("p", result)

def heading_to_html_node(block):
    level = len(block) - len(block.lstrip("#"))
    strip_level = block[level + 1:]
    result = text_to_children(strip_level)
    return ParentNode(f"h{level}", result)

def code_to_html_node(block):
    lines = block.split("\n")
    strip_block = "\n".join(lines[1:-1]) + "\n"
    text_block_node = TextNode(strip_block, TextType.CODE)
    text_html = text_node_to_html_node(text_block_node)
    return ParentNode("pre", [text_html])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        clean = line.lstrip(">").strip()
        new_lines.append(clean)
    clean_line = " ".join(new_lines)
    result = text_to_children(clean_line)
    return ParentNode("blockquote", result)

    

def ulist_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        clean = line[2:]
        children = text_to_children(clean)
        new_lines.append(ParentNode("li", children))
    return ParentNode("ul", new_lines)

def olist_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        parts = line.split(". ", 1)
        clean = parts[1].strip()
        children = text_to_children(clean)
        new_lines.append(ParentNode("li", children))
    return ParentNode("ol", new_lines)