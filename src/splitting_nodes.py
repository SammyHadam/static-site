import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not delimiter:
        raise ValueError("Delimiter cannot be empty or None.")
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_node.append(node)
            continue
        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown Syntax: Delimiter pair not found")
        for i in range (len(parts)):
            if i == 0 or i % 2 == 0:
                new_node.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_node.append(TextNode(parts[i], text_type))
    return new_node

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    for node in old_nodes:
        finding_markdown_image = extract_markdown_images(node)
        new_nodes = old_nodes.split(f"![{finding_markdown_image[0]}]({finding_markdown_image[1]})", 1)
    
def split_nodes_link(old_nodes):
    finding_markdown_link = extract_markdown_links(old_nodes)