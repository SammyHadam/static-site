import unittest
from splitting_nodes import (
    split_nodes_delimiter,
    extract_markdown_images, 
    extract_markdown_links
)

from textnode import TextNode, TextType

class SplitTextNodes(unittest.TestCase):
    def test_text_type(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_basic(self):
        node = TextNode("Hello **world**!", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_delimiter_no_delimiter(self):
        node = TextNode("Hello", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("Hello", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_split_nodes_delimiter_raises_for_unmatched(self):
        node = TextNode("This is **unclosed bold.", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

class MarkDownParser(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

if __name__ == "__main__":
    unittest.main()