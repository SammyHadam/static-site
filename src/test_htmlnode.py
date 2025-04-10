import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_none_for_self_props(self):
        htmlnode = HTMLNode("h1", "This is a heading", [], None)
        self.assertEqual(htmlnode.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()