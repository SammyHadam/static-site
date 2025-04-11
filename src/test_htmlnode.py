import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_none_for_self_props(self):
        htmlnode = HTMLNode("h1", "This is a heading", [], None)
        self.assertEqual(htmlnode.props_to_html(), "")
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )


if __name__ == "__main__":
    unittest.main()