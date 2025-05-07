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


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # Only process TEXT nodes for images
            result.append(node)
            continue
            
        # Process this node
        images = extract_markdown_images(node.text)
        if not images:
            # No images to process
            result.append(node)
        else:
            # Process the first image
            alt_text, url = images[0]
            image_markdown = f"![{alt_text}]({url})"
            parts = node.text.split(image_markdown, 1)
            
            # Add text before image if not empty
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the image node
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Process text after image recursively if not empty
            if parts[1]:
                # Recursively process any remaining images in parts[1]
                remaining_nodes = split_nodes_image([TextNode(parts[1], TextType.TEXT)])
                result.extend(remaining_nodes)
    
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # Only process TEXT nodes for links
            result.append(node)
            continue
            
        # Process this node
        links = extract_markdown_links(node.text)
        if not links:
            # No links to process
            result.append(node)
        else:
            # Process the first link
            text, url = links[0]
            link_markdown = f"[{text}]({url})"  # Removed the exclamation mark
            parts = node.text.split(link_markdown, 1)
            
            # Add text before link if not empty
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the link node
            result.append(TextNode(text, TextType.LINK, url))
            
            # Process text after link recursively if not empty
            if parts[1]:
                # Recursively process any remaining links in parts[1]
                remaining_nodes = split_nodes_link([TextNode(parts[1], TextType.TEXT)])
                result.extend(remaining_nodes)
    
    return result

def text_to_textnodes(text):
    old_nodes = []
    old_nodes.append(TextNode(text, TextType.TEXT))
    images_extracted = split_nodes_image(old_nodes)
    links_extracted = split_nodes_link(images_extracted)
    bold_extracted = split_nodes_delimiter(links_extracted, "**", TextType.BOLD)
    italic_extracted = split_nodes_delimiter(bold_extracted, "_", TextType.ITALIC)
    code_extracted = split_nodes_delimiter(italic_extracted, "`", TextType.CODE)
    return code_extracted


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


