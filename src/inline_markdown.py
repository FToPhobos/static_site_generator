import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for nodes in old_nodes:
        if nodes.text_type is not TextType.TEXT:
            result.append(nodes)   
        else:
            parts = nodes.text.split(delimiter)

            if len(parts) % 2 == 0:
                raise ValueError("invalid Markdown: no closing delimiter found")
    
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    result.append(TextNode(part, TextType.TEXT))
                else:
                    result.append(TextNode(part,text_type))

    return result

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)
        
        if not images:
            new_nodes.append(old_node)
            continue
        
        current_text = old_node.text
        for image_alt, image_link in images:
            image_markdown = f"![{image_alt}]({image_link})"
            
            sections = current_text.split(image_markdown, 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            
            current_text = sections[1]
            
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        
        if not links:
            new_nodes.append(old_node)
            continue
        
        current_text = old_node.text
        for link_alt, link_link in links:
            link_markdown = f"[{link_alt}]({link_link})"
            
            sections = current_text.split(link_markdown, 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
            
            current_text = sections[1]
            
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
